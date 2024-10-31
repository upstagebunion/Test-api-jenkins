import pytest
from app import create_app, db
from app.models import Project
from flask import json

@pytest.fixture
def client():
    # Configuración del entorno de pruebas
    app = create_app("testing")
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Creación de tablas
        yield client
        with app.app_context():
            db.drop_all()  # Limpieza de la base de datos

def get_headers(token=None):
    headers = {
        "Content-Type": "application/json"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def test_create_project(client):
    # Suponiendo que hay un endpoint para autenticación
    auth_response = client.post('/auth', json={"username": "user", "password": "pass"})
    token = auth_response.json["access_token"]

    data = {
        "name": "Proyecto de Prueba",
        "description": "Descripción de prueba para el proyecto"
    }
    response = client.post('/projects', data=json.dumps(data), headers=get_headers(token))
    assert response.status_code == 201
    assert response.json["name"] == data["name"]

def test_get_project(client):
    auth_response = client.post('/auth', json={"username": "user", "password": "pass"})
    token = auth_response.json["access_token"]

    # Crear un proyecto
    project = Project(name="Proyecto Existente", description="Descripción")
    db.session.add(project)
    db.session.commit()

    # Consultar el proyecto
    response = client.get(f'/projects/{project.id}', headers=get_headers(token))
    assert response.status_code == 200
    assert response.json["name"] == "Proyecto Existente"

def test_update_project(client):
    auth_response = client.post('/auth', json={"username": "user", "password": "pass"})
    token = auth_response.json["access_token"]

    # Crear un proyecto para actualizar
    project = Project(name="Proyecto a Actualizar", description="Descripción inicial")
    db.session.add(project)
    db.session.commit()

    # Actualizar el proyecto
    update_data = {
        "name": "Proyecto Actualizado",
        "description": "Nueva descripción"
    }
    response = client.put(f'/projects/{project.id}', data=json.dumps(update_data), headers=get_headers(token))
    assert response.status_code == 200
    assert response.json["name"] == update_data["name"]

def test_delete_project(client):
    auth_response = client.post('/auth', json={"username": "user", "password": "pass"})
    token = auth_response.json["access_token"]

    # Crear un proyecto para eliminar
    project = Project(name="Proyecto a Eliminar", description="Será eliminado")
    db.session.add(project)
    db.session.commit()

    # Eliminar el proyecto
    response = client.delete(f'/projects/{project.id}', headers=get_headers(token))
    assert response.status_code == 204

    # Verificar que ya no existe
    response = client.get(f'/projects/{project.id}', headers=get_headers(token))
    assert response.status_code == 404

def test_create_project_unauthorized(client):
    # Intento de crear un proyecto sin autenticación
    data = {
        "name": "Proyecto no autorizado",
        "description": "Descripción"
    }
    response = client.post('/projects', data=json.dumps(data), headers=get_headers())
    assert response.status_code == 401
