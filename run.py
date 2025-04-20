import schedule
import time
import threading
from app.services import parser_science_news
from app import create_app, db, models

app = create_app()

@app.shell_context_processor
def get_context():
    # Для змоги прописати в консолі 'flask shell'
    # й сразу використовувати 
    # - app (Flask додаток)
    # - db (SQLAlchemy)
    # - models (Доступ до всіх моделок)
    return dict(app=app, db=db, models=models)

schedule.every(18).hours.do(parser_science_news)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    app.run(debug=True)