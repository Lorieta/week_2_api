from fastapi import FastAPI

app = FastAPI()

# Endpoint template form docs

@app.get("/hello")
async def read_root():
    return {"Hello":"World"}

@app.get("/")
async def task_model():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get ("/health")
async def check_health():
    return { "status": "ok" }