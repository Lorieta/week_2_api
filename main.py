from fastapi import FastAPI
from fastapi.responses import JSONResponse
app = FastAPI()

tasks_db = [
    {"id": 1, "title": "Install Python", "done": True},
    {"id": 2, "title": "Build read endpoints", "done": False},
    {"id": 3, "title": "Test uvcorn", "done": False}
]

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
@app.get("/task")
async def get_task():
    if tasks_db :
        return tasks_db
    return JSONResponse(
            status_code=404, 
            content={"error": f"No task exist"}
            )
# Get a specific task
@app.get("/task/{id}")
async def get_task(id:int):
    for task in tasks_db:
        if task["id"] == id:
            return task
    return JSONResponse(
            status_code=404, 
            content={"error": f"Task {id} not found"}
            )