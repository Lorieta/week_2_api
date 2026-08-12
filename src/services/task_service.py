from fastapi import HTTPException
from typing import Optional

from src.repositories import task_repo


def get_all_tasks() -> list[dict]:
    return task_repo.get_all()


def get_task(task_id: int) -> dict:
    task = task_repo.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


def search_tasks(title: Optional[str] = None, done: Optional[bool] = None) -> list[dict]:
    return task_repo.search(title=title, done=done)


def create_task(title: str) -> dict:
    stripped = title.strip()
    if not stripped:
        raise HTTPException(status_code=400, detail="Title is needed")
    return task_repo.create(stripped)


def update_task(task_id: int, title: Optional[str] = None, done: Optional[bool] = None) -> dict:
    if title is not None:
        stripped = title.strip()
        if not stripped:
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        title = stripped
    task = task_repo.update(task_id, title=title, done=done)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


def delete_task(task_id: int) -> bool:
    deleted = task_repo.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return True
