from datetime import datetime

from pydantic import BaseModel


class WarningBadge(BaseModel):
    id: str
    label: str
    description: str
    severity: str


class InputStats(BaseModel):
    word_count: int
    character_count: int
    reading_time_minutes: int


class AnalysisBase(BaseModel):
    id: int
    created_at: datetime
    title: str
    label: str
    verdict: str
    risk_band: str
    fake_probability: float
    confidence_percent: float
    advisory_note: str
    input_stats: InputStats
    warning_badges: list[WarningBadge]
    source_type: str
    source_name: str | None = None


class AnalysisListItem(AnalysisBase):
    article_preview: str


class AnalysisDetail(AnalysisBase):
    article_text: str


class HealthCheck(BaseModel):
    status: str


class ValidationErrorResponse(BaseModel):
    detail: str
