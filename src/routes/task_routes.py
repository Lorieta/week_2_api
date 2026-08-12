from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Optional

from src.models import TaskCreate, TaskUpdate
from src.services import task_service

router = APIRouter()


@router.get("/hello")
async def read_root():
    return {"Hello": "World"}


@router.get("/")
async def task_model():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@router.get("/health")
async def check_health():
    return {"status": "ok"}


@router.get("/tasks")
async def get_all_task():
    tasks = task_service.get_all_tasks()
    if tasks:
        return tasks
    return JSONResponse(status_code=404, content={"error": "No task exist"})


@router.get("/tasks/{id}")
async def get_task(id: int):
    return task_service.get_task(id)


@router.get("/tasks/")
async def search_task(
    title: Optional[str] = Query(None),
    done: Optional[bool] = Query(None),
):
    return task_service.search_tasks(title=title, done=done)


@router.post("/tasks", status_code=201)
async def add_task(payload: TaskCreate):
    task = task_service.create_task(payload.title)
    return {"status": "Created", "task": task}


@router.put("/tasks/{id}")
async def update_task(id: int, update: TaskUpdate):
    return task_service.update_task(id, title=update.title, done=update.done)


@router.delete("/tasks/{id}", status_code=204)
async def delete_task(id: int):
    task_service.delete_task(id)
