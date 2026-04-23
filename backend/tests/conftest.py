from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.database import Base, build_engine, get_db
from app.main import app
from app.services.classifier import get_classifier


class StubClassifier:
    def predict_fake_probability(self, title: str, article_text: str) -> float:
        combined = f"{title} {article_text}".lower()
        if "fabricated" in combined or "shocking" in combined:
            return 0.89
        return 0.16


@pytest.fixture
def client(tmp_path: Path):
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    engine = build_engine(database_url)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_classifier] = lambda: StubClassifier()

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
