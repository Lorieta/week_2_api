from fastapi import FastAPI
from services.db import get_connection, init_db, seeding
from routes.task_routes import router as task_router

import uvicorn

def create_app() -> FastAPI:
    app = FastAPI(title="Backend AI Assignment")
    app.include_router(task_router)
    return app


if __name__ == "__main__":
    app = create_app()
    conn = get_connection()
    try:
        init_db(conn)
        seeding(conn)
    finally:
        conn.close()

uvicorn.run(app, host="127.0.0.1", port=3000)

