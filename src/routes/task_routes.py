from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from sqlite3 import IntegrityError
from models import TaskCreate, TaskUpdate, Task
from services import task_service
from services.db import get_connection

router = APIRouter()


def get_conn():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


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
async def get_all_task(conn=Depends(get_conn)):
    tasks = task_service.get_all_tasks(conn)
    if tasks:
        return tasks
    return JSONResponse(status_code=404, content={"error": "No task exist"})


@router.get("/tasks/{id}")
async def get_task(id: int, conn=Depends(get_conn)):
    return task_service.get_task(id, conn)


@router.get("/tasks/")
async def search_task(title, conn=Depends(get_conn)):
    return task_service.search_tasks(conn, title)


@router.post("/tasks", response_model=Task, status_code=201)
async def add_task(payload: TaskCreate, conn=Depends(get_conn)):
    task_data = task_service.create_task(
        conn=conn,
        title=payload.title,
        done=payload.done
    )
    return task_data


@router.put("/tasks/{id}")
async def update_task(id: int, update: TaskUpdate, conn=Depends(get_conn)):
    rows = task_service.update_task(conn, id, title=update.title, done=update.done)
    if rows == -1:
        return JSONResponse(status_code=409, content={"error": "Title already exists"})
    if rows:
        return JSONResponse(status_code=200, content={"message": "Task updated"})
    return JSONResponse(status_code=404, content={"error": "No task exist"})


@router.delete("/tasks/{id}", status_code=204)
async def delete_task(id: int, conn=Depends(get_conn)):
    rows = task_service.delete_task(conn, id)
    if not rows:
        return JSONResponse(status_code=404, content={"error": "No task exist"})
