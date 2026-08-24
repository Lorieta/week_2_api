from fastapi import HTTPException
from typing import Optional

from models import Task
from services import db
from sqlite3 import IntegrityError

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

#Search
def search_tasks(conn, q: str):
    curr = conn.cursor()
    statement = "SELECT * FROM tasks WHERE title LIKE :search_term"
    
    wildcard_query = f"%{q}%"
    
    result = curr.execute(statement, {"search_term": wildcard_query}).fetchall()
    
   
    return result


def create_task(conn,title:str, done: int ):
    if not title:
        raise HTTPException(status_code=400, detail="Title is needed")
    
    try:
        curr = conn.cursor()
        statement   = "INSERT INTO tasks (title, done) VALUES (:title, :done)"
   
        curr.execute(statement, {"title": title, "done": done})
        conn.commit()
        task_id = curr.lastrowid
    except IntegrityError:
        conn.rollback()
        raise HTTPException(
            status_code=409, 
            detail=f"A task with the title '{title}' already exists."
        )
    return {"id": task_id, "title": title, "done": done}


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
