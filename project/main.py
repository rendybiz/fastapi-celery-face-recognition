from celery.result  import AsyncResult
from fastapi        import Body, FastAPI, Form, Request
from fastapi.responses      import JSONResponse
from fastapi.staticfiles    import StaticFiles
from fastapi.templating     import Jinja2Templates
from fastapi.middleware.cors    import CORSMiddleware
from worker import face_recognition_task, redis_key_clean_up_task

import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug-info.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

app = FastAPI()
# app.mount("/static", StaticFiles(directory="project/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home(request: Request):
    return JSONResponse({"message": "Welcome to Face recognition REST", "response": "OK"})

@app.get("/face_recognition/")
def get_validate():
    task = face_recognition_task.delay({"data": "data"})
    return JSONResponse({"task_id": task.id, "response": "OK"})

@app.get("/redis_key_clean_up/")
def get_redis_key_clean_up_task():
    task = redis_key_clean_up_task.delay({"data": "data"})
    return JSONResponse({"task_id": task.id, "response": "OK"})
