# TaskFlow - Система управления задачами

Веб-приложение для управления персональными задачами с автоматизированным пайплайном развертывания.

## Технологический стек

- **Backend**: Python (Flask), REST API
- **Frontend**: HTML5, CSS3, JavaScript (Jinja2)
- **База данных**: PostgreSQL / SQLite
- **Контейнеризация**: Docker
- **CI/CD**: GitHub Actions
- **WSGI Server**: Gunicorn

## Локальный запуск

### С Docker (рекомендуется):
```bash
docker-compose up --build

Без Docker:
bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

pip install -r requirements.txt
python init_db.py
python run.py
