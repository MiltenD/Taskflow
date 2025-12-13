from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app import db
from app.models import Task, Category
from datetime import datetime, timezone

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/tasks')
def tasks():
    category_filter = request.args.get('category')
    status_filter = request.args.get('status')
    priority_filter = request.args.get('priority')
    
    tasks_query = Task.query
    
    if category_filter and category_filter != 'all':
        tasks_query = tasks_query.filter_by(category_id=category_filter)
    if status_filter and status_filter != 'all':
        tasks_query = tasks_query.filter_by(status=status_filter)
    if priority_filter and priority_filter != 'all':
        tasks_query = tasks_query.filter_by(priority=priority_filter)
    
    tasks = tasks_query.order_by(Task.created_at.desc()).all()
    categories = Category.query.all()
    
    return render_template('tasks.html', tasks=tasks, categories=categories)

@main.route('/api/tasks', methods=['GET'])
def get_tasks_api():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@main.route('/api/tasks', methods=['POST'])
def create_task_api():
    data = request.get_json()
    
    task = Task(
        title=data.get('title'),
        description=data.get('description'),
        status=data.get('status', 'pending'),
        priority=data.get('priority', 'medium'),
        category_id=data.get('category_id')
    )
    
    if data.get('due_date'):
        task.due_date = datetime.fromisoformat(data.get('due_date'))
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201

@main.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task_api(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.priority = data.get('priority', task.priority)
    task.category_id = data.get('category_id', task.category_id)
    
    if data.get('due_date'):
        task.due_date = datetime.fromisoformat(data.get('due_date'))
    
    db.session.commit()
    
    return jsonify(task.to_dict())

@main.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task_api(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'message': 'Task deleted successfully'})

@main.route('/add-task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority', 'medium')
        category_id = request.form.get('category_id')
        
        task = Task(
            title=title,
            description=description,
            priority=priority,
            category_id=category_id if category_id else None
        )
        
        db.session.add(task)
        db.session.commit()
        
        flash('Task added successfully!', 'success')
        return redirect(url_for('main.tasks'))
    
    categories = Category.query.all()
    return render_template('add_task.html', categories=categories)

@main.route('/health')
def health_check():
    try:
        # Проверка подключения к БД
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 500

# Добавление тестовых категорий
@main.route('/init-db')
def init_db():
    """Эндпоинт для инициализации тестовых данных"""
    categories = ['Work', 'Personal', 'Shopping', 'Health', 'Education']
    
    for cat_name in categories:
        if not Category.query.filter_by(name=cat_name).first():
            category = Category(name=cat_name)
            db.session.add(category)
    
    db.session.commit()
    return jsonify({'message': 'Database initialized with sample categories'})