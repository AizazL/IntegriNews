def test_analyze_persists_record_and_returns_result(client):
    response = client.post(
        "/analyze",
        data={
            "title": "Shocking fabricated claim",
            "body": "This fabricated article copy is designed to trigger a high fake score.",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["title"] == "Shocking fabricated claim"
    assert payload["label"] == "fake"
    assert payload["input_stats"]["word_count"] > 0

    listing = client.get("/analyses")
    assert listing.status_code == 200
    assert len(listing.json()) == 1


def test_analyze_validates_missing_body_and_upload(client):
    response = client.post("/analyze", data={"title": "Incomplete submission"})
    assert response.status_code == 422
    assert response.json()["detail"] == "A title and article body or supported upload are required."


def test_get_analysis_returns_saved_record(client):
    created = client.post(
        "/analyze",
        data={"title": "Credible local reporting", "body": "This article includes sourcing and balanced claims."},
    ).json()

    response = client.get(f"/analyses/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_export_csv_returns_saved_rows(client):
    client.post("/analyze", data={"title": "Export me", "body": "A short article body for export coverage."})

    response = client.get("/analyses/export.csv")

    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "Export me" in response.text
