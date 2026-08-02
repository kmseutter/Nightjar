from fastapi import FastAPI
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import Field, Session, SQLModel, create_engine, select
import uvicorn
#bad practice to use *, info may be shared when not meant to#
from src.models import *

app = FastAPI(title="User Auth API")

# The login payload
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/user/login")
async def login(credentials: LoginRequest):
    # In a real app, you would hash the password and check it against a database here.
    return {
        "message": f"Welcome, {credentials.username}",
        "token": "example-jwt-token-123456"
    }

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

class Settings(BaseSettings):
    # Example for .env file: database_url=postgresql://user:password@10.0.0.66:5432/nightjardev
    database_url: str
    debug_mode: bool = False

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

engine = create_engine(settings.database_url)
SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
