from fastapi import HTTPException
from typing import Optional


from services import db

def get_all_tasks(conn) -> list[dict]:
    curr = conn.cursor()
    statement = """
    SELECT * FROM tasks
    """
    result = curr.execute(statement).fetchall()
    return result


def get_task(task_id: int,conn):
    curr = conn.cursor()
    statement = "SELECT * FROM tasks WHERE id = ?"
    result = curr.execute(statement,(task_id,)).fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return result


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
