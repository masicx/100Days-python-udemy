import pytest

from main import app, db, ToDo


@pytest.fixture()
def client():
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")

    with app.app_context():
        db.drop_all()
        db.create_all()
        todo = ToDo(text="Test task", dueDate="", isChecked=False, createdAt="2024-01-01")
        db.session.add(todo)
        db.session.commit()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_check_toggle_updates_status(client):
    response = client.post("/check/1")

    assert response.status_code == 200

    with app.app_context():
        todo = db.session.get(ToDo, 1)
        assert todo is not None
        assert todo.isChecked is True
