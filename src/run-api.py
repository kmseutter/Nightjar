from fastapi import FastAPI
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
import uvicorn

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
        "token": "example-jwt-token-12345"
    }

@app.post("/user/logout")
async def logout():
    # In a real app, you would invalidate the session or JWT here.
    return {
        "message": "Successfully logged out"
    }


class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    debug_mode: bool = False

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)