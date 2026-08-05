from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, StrictBool, StrictStr


class Task(BaseModel):
    id: int
    title: str
    done: bool = False


class TaskCreate(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    title: StrictStr


class TaskUpdate(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    title: Optional[StrictStr] = None
    done: Optional[StrictBool] = None


app = FastAPI(title="Task API")

tasks_db: dict[int, Task] = {}
next_task_id = 1


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )


@app.get("/tasks", status_code=200)
async def list_tasks():
    return list(tasks_db.values())


@app.post("/tasks", status_code=201)
async def create_task(payload: TaskCreate):
    global next_task_id

    title = payload.title.strip()
    if not title:
        raise HTTPException(
            status_code=400,
            detail="Title is required and cannot be empty or whitespace",
        )

    task = Task(id=next_task_id, title=title, done=False)
    tasks_db[next_task_id] = task
    next_task_id += 1
    return task


@app.get("/tasks/{task_id}", status_code=200)
async def get_task(task_id: int):
    task = tasks_db.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.put("/tasks/{task_id}", status_code=200)
async def update_task(task_id: int, payload: TaskUpdate):
    task = tasks_db.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    if payload.title is not None:
        title = payload.title.strip()
        if not title:
            raise HTTPException(
                status_code=400,
                detail="Title is required and cannot be empty or whitespace",
            )
        task = task.model_copy(update={"title": title})

    if payload.done is not None:
        task = task.model_copy(update={"done": payload.done})

    tasks_db[task_id] = task
    return task


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    del tasks_db[task_id]
