from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette import status
from starlette.responses import RedirectResponse

from models import Base
from database import engine
from routers.auth import router as auth_router
from routers.todo import router as todo_router
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth_router)#oluşturduğumuz routerı app içine dahil etmek için
app.include_router(todo_router)


@app.get("/")
async def read_root(request: Request):
    return RedirectResponse(url="/todo/todo-page", status_code=status.HTTP_302_FOUND)

Base.metadata.create_all(bind = engine)