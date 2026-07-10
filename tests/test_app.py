import pytest

from app import app as flask_app


@pytest.fixture()
def client():
    flask_app.config.update(TESTING=True)
    with flask_app.test_client() as test_client:
        yield test_client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Flask CI/CD App" in response.data
