from contextlib import asynccontextmanager
from csv import DictWriter
from io import StringIO

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from .config import get_settings
from .database import get_db, init_db
from .models import AnalysisRecord
from .schemas import AnalysisDetail, AnalysisListItem, HealthCheck, ValidationErrorResponse
from .services.classifier import build_analysis_summary, get_classifier, merge_article_sources
from .services.file_parser import UnsupportedFileTypeError, extract_text_from_upload


def serialize_analysis(record: AnalysisRecord, include_full_text: bool = False) -> dict[str, object]:
    payload: dict[str, object] = {
        "id": record.id,
        "created_at": record.created_at,
        "title": record.title,
        "label": record.label,
        "verdict": record.verdict,
        "risk_band": record.risk_band,
        "fake_probability": record.fake_probability,
        "confidence_percent": record.confidence_percent,
        "advisory_note": record.advisory_note,
        "input_stats": {
            "word_count": record.word_count,
            "character_count": record.character_count,
            "reading_time_minutes": record.reading_time_minutes,
        },
        "warning_badges": record.warning_badges,
        "source_type": record.source_type,
        "source_name": record.source_name,
    }

    if include_full_text:
        payload["article_text"] = record.article_text
    else:
        payload["article_preview"] = record.article_text[:240].strip() + ("..." if len(record.article_text) > 240 else "")

    return payload


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthCheck)
def healthcheck() -> HealthCheck:
    return HealthCheck(status="ok")


@app.post(
    "/analyze",
    response_model=AnalysisDetail,
    responses={422: {"model": ValidationErrorResponse}},
)
async def analyze_article(
    title: str = Form(...),
    body: str | None = Form(default=None),
    file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
    classifier=Depends(get_classifier),
):
    uploaded_text: str | None = None
    source_type = "manual"
    source_name: str | None = None

    if file is not None and file.filename:
        source_type = "upload"
        source_name = file.filename
        try:
            uploaded_text = await extract_text_from_upload(file)
        except UnsupportedFileTypeError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    article_text = merge_article_sources(body, uploaded_text)
    if not title.strip() or not article_text.strip():
        raise HTTPException(status_code=422, detail="A title and article body or supported upload are required.")

    fake_probability = classifier.predict_fake_probability(title, article_text)
    summary = build_analysis_summary(title, article_text, fake_probability)

    record = AnalysisRecord(
        title=title.strip(),
        article_text=article_text.strip(),
        label=str(summary["label"]),
        verdict=str(summary["verdict"]),
        risk_band=str(summary["risk_band"]),
        fake_probability=float(summary["fake_probability"]),
        confidence_percent=float(summary["confidence_percent"]),
        word_count=int(summary["input_stats"]["word_count"]),
        reading_time_minutes=int(summary["input_stats"]["reading_time_minutes"]),
        character_count=int(summary["input_stats"]["character_count"]),
        warning_badges=list(summary["warning_badges"]),
        advisory_note=str(summary["advisory_note"]),
        source_type=source_type,
        source_name=source_name,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return serialize_analysis(record, include_full_text=True)


@app.get("/analyses", response_model=list[AnalysisListItem])
def list_analyses(limit: int = 25, db: Session = Depends(get_db)):
    bounded_limit = min(max(limit, 1), 100)
    records = db.scalars(select(AnalysisRecord).order_by(AnalysisRecord.created_at.desc()).limit(bounded_limit)).all()
    return [serialize_analysis(record) for record in records]


@app.get("/analyses/export.csv")
def export_analyses(db: Session = Depends(get_db)):
    records = db.scalars(select(AnalysisRecord).order_by(AnalysisRecord.created_at.desc())).all()
    output = StringIO()
    writer = DictWriter(
        output,
        fieldnames=[
            "id",
            "created_at",
            "title",
            "label",
            "verdict",
            "risk_band",
            "fake_probability",
            "confidence_percent",
            "word_count",
            "reading_time_minutes",
            "character_count",
            "source_type",
            "source_name",
        ],
    )
    writer.writeheader()
    for record in records:
        writer.writerow(
            {
                "id": record.id,
                "created_at": record.created_at.isoformat(),
                "title": record.title,
                "label": record.label,
                "verdict": record.verdict,
                "risk_band": record.risk_band,
                "fake_probability": record.fake_probability,
                "confidence_percent": record.confidence_percent,
                "word_count": record.word_count,
                "reading_time_minutes": record.reading_time_minutes,
                "character_count": record.character_count,
                "source_type": record.source_type,
                "source_name": record.source_name or "",
            }
        )
    output.seek(0)
    headers = {"Content-Disposition": "attachment; filename=integri-news-analyses.csv"}
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers=headers)


@app.get("/analyses/{analysis_id}", response_model=AnalysisDetail)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    record = db.get(AnalysisRecord, analysis_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    return serialize_analysis(record, include_full_text=True)
