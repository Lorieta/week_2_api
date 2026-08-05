from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Body, HTTPException
from pydantic import BaseModel
from typing import Optional
class Task(BaseModel):
    id: int
    title: str
    done: bool

class TaskCreate(BaseModel):
    title:str
    

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

app = FastAPI()

tasks_db = [
    {"id": 1, "title": "Install Python", "done": True},
    {"id": 2, "title": "Build read endpoints", "done": False},
    {"id": 3, "title": "Test uvcorn", "done": False}
]

next_task_id = max(task["id"] for task in tasks_db) + 1

# Endpoint template form docs
@app.get("/hello")
async def read_root():
    return {"Hello":"World"}

# Describe the API
@app.get("/")
async def task_model():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

#Check health
@app.get ("/health")
async def check_health():
    return { "status": "ok" }

#List all task
@app.get("/tasks")
async def get_all_task():
    if tasks_db :
        return tasks_db
    return JSONResponse(
            status_code=404, 
            content={"error": f"No task exist"}
            )
# Get a specific task
@app.get("/tasks/{id}")
async def get_task(id:int):
    for task in tasks_db:
        if task["id"] == id:
            return task
    return JSONResponse(
            status_code=404, 
            content={"error": f"Task {id} not found"}
            )
# Add
@app.post("/tasks", status_code=201)
async def add_task(payload: TaskCreate):
    global next_task_id
    
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title is needed")
    
    new_task = {
        "id": next_task_id,
        "title": title,
        "done": False
    }
    tasks_db.append(new_task)
    next_task_id += 1
    
    return {"status": "Created", "task": new_task}

@app.put("/tasks/{id}")
async def update_task(id: int, update: TaskUpdate):
    for task in tasks_db:
        if task["id"] == id:
            
            if update.title is not None:
                stripped = update.title.strip()
                if not stripped:
                    raise HTTPException(status_code=400, detail="Title cannot be empty")
                task["title"] = stripped
            if update.done is not None:
                task["done"] = update.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {id} not found")

#delete
@app.delete("/tasks/{id}",status_code=204)
async def delete_task(id: int):
    for task in tasks_db:
        if task["id"] == id:
            tasks_db.remove(task)
            return  {f"Task {id} Deleted"}
    raise HTTPException(status_code=404, detail=f"Task {id} not found")