import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app_sofware')))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"<title>" in rv.data or b"Inicio" in rv.data

def test_register_page(client):
    rv = client.get('/register')
    assert rv.status_code == 200
    assert b"username" in rv.data or b"Registro" in rv.data

def test_login_page(client):
    rv = client.get('/login')
    assert rv.status_code == 200
    assert b"username" in rv.data or b"Login" in rv.data

def test_dashboard_requires_login(client):
    rv = client.get('/dashboard')
    # debe redirigir a login si no está logueado
    assert rv.status_code == 302
    assert '/login' in rv.headers['Location']
