import pytest
from app import create_app
from app.models import db, Student, Project

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_student(client):
    response = client.post('/api/students', json={
        'name': 'John Doe',
        'email': 'johndoe@example.com'
    })
    assert response.status_code == 201
