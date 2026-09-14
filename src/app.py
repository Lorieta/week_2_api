from fastapi import FastAPI
from src.services.db import get_connection, init_db, seeding
from src.routes.task_routes import router as task_router

import time

def wait_for_db(max_retries=10, delay=2):
    for i in range(max_retries):
        try:
            return get_connection()
        except Exception:
            print(f"DB not ready, retrying in {delay}s...")
            time.sleep(delay)
    raise Exception("Could not connect to database")

def create_app() -> FastAPI:
    app = FastAPI(title="Backend AI Assignment")
    app.include_router(task_router)
    return app

app = create_app()

conn = wait_for_db()
init_db(conn)
seeding(conn)
conn.close()

   

