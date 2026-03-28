from datetime import timedelta, datetime, timezone
from typing import Annotated

from aiofiles.os import access
from fastapi import APIRouter, Depends, HTTPException,Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status


from ..database import SessionLocal#aynı directoryde olmadıkları için 2 nokta
from ..models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/auth",#bütün endpointlerin başına /auth ekledi
    tags=["auth"],#swaggerda ayrı olarak görmemizi sağladı
)

templates = Jinja2Templates(directory="app/templates")
SECRET_KEY = "a2jll2xpi9zrn7nvey5wd8d6snacim09"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db #return gibi dbyi döndürür farkı yield kullanılan fonsiyonlara generator deriz
                    # return 1 döndürüyorsa yield daha çok veri döndürebilir
    finally:
        db.close()#sessionı kapatmak için


db_dependency = Annotated[Session,Depends(get_db)]

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str

class Token(BaseModel):
    access_token: str
    token_type: str

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, role:str, expires_delta: timedelta):
    encode = {"sub":username, "id":user_id, "role":role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode( token,SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        user_id = payload.get("id")
        user_role = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or id is invalid.")
        return {"username": username, "id": user_id, "role": user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid.")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db : db_dependency, create_user_request: CreateUserRequest):
    user = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        is_active= True,
        hashed_password=bcrypt_context.hash(create_user_request.password),#bu şekilde şifrelenmiş şekilde alıcaz
        phone_number=create_user_request.phone_number
    )
    db.add(user)
    db.commit()

@router.get("/login-page")
def read_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register-page")
def read_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=60))
    return {"access_token": token, "token_type": "bearer"}#bearer tokenları isteğin gerçektewn kullanıcı tarafından geldiğini gösteren token tipi



