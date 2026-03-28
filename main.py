from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette import status
from starlette.responses import RedirectResponse

from .models import Base,Todo
from .database import engine
from .routers.auth import router as auth_router
from .routers.todo import router as todo_router
import os
app = FastAPI()

script_dir = os.path.dirname(__file__)#şuan çalıştığı klasör neyse bu kodla alabilecek
st_abs_file_path = os.path.join(script_dir, "static/")

app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")
app.include_router(auth_router)#oluşturduğumuz routerı app içine dahil etmek için
app.include_router(todo_router)


@app.get("/")
async def read_root(request: Request):
    return RedirectResponse(url="/todo/todo-page", status_code=status.HTTP_302_FOUND)

Base.metadata.create_all(bind = engine)