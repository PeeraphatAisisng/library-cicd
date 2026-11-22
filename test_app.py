import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_home_page_lists_sample_books(client):
    page = client.get("/").get_data(as_text=True)
    assert "Clean Code" in page
    assert "ระบบยืม-คืนหนังสือ" in page


def test_health_check(client):
    data = client.get("/health").get_json()
    assert data["status"] == "ok"
    assert data["total"] == 3


def test_add_borrow_and_return_flow(client):
    client.post("/books", data={"title": "Docker", "author": "Nigel"})
    assert client.get("/health").get_json()["total"] == 4
    client.post("/books/4/borrow", data={"borrower": "Peeraphat"})
    assert client.get("/health").get_json()["borrowed"] == 1
    client.post("/books/4/return")
    assert client.get("/health").get_json()["borrowed"] == 0


def test_error_message_is_shown(client):
    page = client.post("/books/1/return", follow_redirects=True).get_data(as_text=True)
    assert "ยังไม่ได้ถูกยืม" in page
