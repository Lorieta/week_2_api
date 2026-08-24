# from typing import Optional
# #old Version

# tasks_db: list[dict] = [
#     {"id": 1, "title": "Install Python", "done": True},
#     {"id": 2, "title": "Build read endpoints", "done": False},
#     {"id": 3, "title": "Test uvcorn", "done": False},
# ]

# next_task_id: int = max(task["id"] for task in tasks_db) + 1


# def get_all() -> list[dict]:
#     return tasks_db


# def get_by_id(task_id: int) -> Optional[dict]:
#     for task in tasks_db:
#         if task["id"] == task_id:
#             return task 
#     return None


# def search(title: Optional[str] = None, done: Optional[bool] = None) -> list[dict]:
#     result = tasks_db.copy()
#     if done is not None:
#         result = [t for t in result if t["done"] == done]
#     if title:
#         result = [t for t in result if title.lower() in t["title"].lower()]
#     return result


# def create(title: str) -> dict:
#     global next_task_id
#     new_task = {"id": next_task_id, "title": title, "done": False}
#     tasks_db.append(new_task)
#     next_task_id += 1
#     return new_task


# def update(task_id: int, title: Optional[str] = None, done: Optional[bool] = None) -> Optional[dict]:
#     task = get_by_id(task_id)
#     if task is None:
#         return None
#     if title is not None:
#         task["title"] = title
#     if done is not None:
#         task["done"] = done
#     return task


# def delete(task_id: int) -> bool:
#     task = get_by_id(task_id)
#     if task is None:
#         return False
#     tasks_db.remove(task)
#     return True
