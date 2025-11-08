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
    assert response.status_code == 200
    assert b'healthy' in response.data

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