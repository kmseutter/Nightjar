from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import Field, Session, SQLModel, create_engine, select
import uvicorn
#bad practice to use *, info may be shared when not meant to#
from src.database import engine, SessionDep
from src.models import *
from src.secure import router as secure_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Anything to run during startup
    SQLModel.metadata.create_all(engine)
    yield
    # Anything to run during shutdown

app = FastAPI(title="User Auth API", lifespan=lifespan)
app.include_router(secure_router)

# The login payload
class LoginRequest(BaseModel):
    username: str
    password: str

# Register payload
class RegisterRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

@app.post("/user/register", response_model = UserResponse, status_code= status.HTTP_201_CREATED)
def register(payload: RegisterRequest):
    with Session(engine) as session:
        existing_user = session.exec(select(Users).where(Users.username == payload.username)).first()
        if existing_user:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail = "Username already registered"
            )
        
        user = Users(
            username = payload.username,
            password = hash_password(payload.password)
        )

        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@app.post("/user/login")
async def login(credentials: LoginRequest):

    with Session(engine) as session:
        statement = select(Users).where(Users.username == credentials.username)
        user = session.exec(statement).first()
        if not user or not verify_password(credentials.password, user.password):
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Invalid username or password"
            )
        return {"message": f"Successfully authenticated as user {user.username}"}

@app.post("/user/logout")
async def logout():
    # In a real app, you would invalidate the session or JWT here.
    return {
        "message": "Successfully logged out"
    }

@app.get("/user")
async def user_get():
    with Session(engine) as session:
        statement = select(Users).where(Users.id == 1)
        results = session.exec(statement)
        user = results.first()

@app.get("/user/{user_id}")
async def user_get(user_id: int):
    with Session(engine) as session:
        statement = select(Users).where(Users.id == user_id)
        results = session.exec(statement)
        user = results.first()
    return user.model_dump()
    return {
        user.id,
        user.name
    }

@app.get("/organization/{org_id}")
async def org_get(org_id: int):
    with Session(engine) as session:
        statement = select(Organizations).where(Organizations.id == org_id)
        results = session.exec(statement)
        org = results.first()
    return org.model_dump()
    return {
        org.id,
        org.name
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
