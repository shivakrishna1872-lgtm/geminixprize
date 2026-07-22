from fastapi.testclient import TestClient

from antigravity_api.main import create_app


def test_health_endpoint_reports_agent_foundation() -> None:
    client = TestClient(create_app())

    response = client.get("/v1/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["service"] == "antigravity-api"
    assert payload["status"] == "ok"
    assert "agent:ceo" in payload["capabilities"]
    assert "agent:support" in payload["capabilities"]
