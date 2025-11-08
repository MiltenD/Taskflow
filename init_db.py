from app import create_app, db
from app.models import Category

def init_database():
    app = create_app()
    
    with app.app_context():
        # Создаем все таблицы
        db.create_all()
        
        # Добавляем стандартные категории
        categories = ['Work', 'Personal', 'Shopping', 'Health', 'Education']
        
        for cat_name in categories:
            if not Category.query.filter_by(name=cat_name).first():
                category = Category(name=cat_name)
                db.session.add(category)
                print(f"Added category: {cat_name}")
        
        db.session.commit()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()