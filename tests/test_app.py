import os

os.environ["DATA_DIR"] = "/tmp/hw1-test-data"

from app import app  # noqa: E402


def test_health():
    res = app.test_client().get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_greet_uses_name():
    res = app.test_client().get("/greet?name=Kemal")
    assert "Kemal" in res.get_json()["message"]
