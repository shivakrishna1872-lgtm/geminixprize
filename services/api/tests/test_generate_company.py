from fastapi.testclient import TestClient

from antigravity_api.main import create_app


def test_generate_company_requires_internal_api_key() -> None:
    client = TestClient(create_app())

    response = client.post("/v1/companies/generate", json={"idea": "build me a waterbottle company"})

    assert response.status_code == 401


def test_generate_company_returns_blueprint_with_internal_api_key() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/v1/companies/generate",
        headers={"X-Antigravity-Api-Key": "dev-antigravity-internal-key"},
        json={"idea": "build me a waterbottle company"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["company_name"]
    assert payload["starter_products"]
    assert payload["status"]
