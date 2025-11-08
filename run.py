from app import create_app, db
from app.models import Task, Category

app = create_app()

@app.cli.command("init-db")
def init_db_command():
    """Инициализация базы данных с тестовыми категориями"""
    categories = ['Work', 'Personal', 'Shopping', 'Health', 'Education']
    
    for cat_name in categories:
        if not Category.query.filter_by(name=cat_name).first():
            category = Category(name=cat_name)
            db.session.add(category)
    
    db.session.commit()
    print("Database initialized with sample categories")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)