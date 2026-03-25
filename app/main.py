from fastapi import FastAPI
from app.Database.Postgres_connection_engine import engine
from sqlmodel import  SQLModel
from .routers import users, authentication


app = FastAPI()

SQLModel.metadata.create_all(engine)

app.include_router(users.router)
app.include_router(authentication.router)

@app.get("/")
async def root():
    return "hello"




