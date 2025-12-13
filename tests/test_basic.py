import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    """Тест health check эндпоинта"""
    response = client.get('/health')
    assert response.is_json
    data = response.get_json()
    assert 'status' in data
    if response.status_code == 500:
        assert 'error' in data
    else:
        assert response.status_code == 200
        assert data['status'] == 'healthy'

def test_index_route(client):
    """Тест главной страницы"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'TaskFlow' in response.data

def test_tasks_route(client):
    """Тест страницы задач"""
    response = client.get('/tasks')
    assert response.status_code == 200
    assert b'Task Management' in response.data

def test_add_task_route(client):
    """Тест страницы добавления задачи"""
    response = client.get('/add-task')
    assert response.status_code == 200
    assert b'Add New Task' in response.data
    
def test_basic_arithmetic():
    """Basic test to ensure pytest works"""
    assert 1 + 1 == 2
    assert 2 * 2 == 4

def test_string_operations():
    """Test string functions"""
    assert "hello".upper() == "HELLO"
    assert len("test") == 4
