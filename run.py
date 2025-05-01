import schedule
import time
import threading
import logging

from app.controllers import savef_news
from app import create_app, db, models


app = create_app()

def run_scheduler():
    with app.app_context():
        schedule.every(1).hours.do(run_with_context, savef_news)
        # Для правильной роботи savef_news потрібен хоч один админ
        while True:
            schedule.run_pending()
            time.sleep(1)
            
def run_with_context(job_func):
    with app.app_context():
        try:
            job_func()
        except Exception as e:
            logging.error(f"Помилка в scheduled завданні: {str(e)}")

@app.shell_context_processor
def get_context():
    # Для змоги прописати в консолі 'flask shell'
    # й сразу використовувати 
    # - app (Flask додаток)
    # - db (SQLAlchemy)
    # - models (Доступ до всіх моделок)
    print("Shell context loaded")
    return dict(app=app, db=db, models=models)#(promote_user_to_admin=promote_user_to_admin)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    app.run(debug=True)