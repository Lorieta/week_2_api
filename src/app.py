from fastapi import FastAPI

from src.routes.task_routes import router as task_router


def create_app() -> FastAPI:
    app = FastAPI(title="Backend AI Assignment")
    app.include_router(task_router)
    return app


app = create_app()
