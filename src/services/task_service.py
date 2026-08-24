from fastapi import HTTPException
from typing import Optional

from models import Task
from services import db
from sqlite3 import IntegrityError


def get_all_tasks(conn) -> list[dict]:
    try:
        curr = conn.cursor()
        result = curr.execute("SELECT * FROM tasks").fetchall()
    except:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return result


def get_task(task_id: int, conn):
    try:
        curr = conn.cursor()
        result = curr.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    except:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    if not result:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return result


def search_tasks(conn, q: str):
    try:
        curr = conn.cursor()
        result = curr.execute("SELECT * FROM tasks WHERE title LIKE :search_term", {"search_term": f"%{q}%"}).fetchall()
    except:
        raise HTTPException(status_code=404, detail=f"No task {q} found")
    return result


def create_task(conn, title: str, done: int):
    if not title:
        raise HTTPException(status_code=400, detail="Title is needed")
    try:
        curr = conn.cursor()
        curr.execute("INSERT INTO tasks (title, done) VALUES (:title, :done)", {"title": title, "done": done})
        conn.commit()
        task_id = curr.lastrowid
    except IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=409, detail=f"A task with the title '{title}' already exists.")
    return {"id": task_id, "title": title, "done": done}


def update_task(conn, task_id: int, title: Optional[str] = None, done: Optional[bool] = None) -> int:
    try:
        curr = conn.cursor()
        curr.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (title, done, task_id))
        conn.commit()
        return curr.rowcount
    except IntegrityError:
        conn.rollback()
        return -1


def delete_task(conn, task_id: int) -> int:
    try:
        curr = conn.cursor()
        curr.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return curr.rowcount
    except:
        conn.rollback()
        return 0
