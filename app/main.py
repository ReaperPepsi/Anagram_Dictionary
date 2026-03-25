from fastapi import FastAPI
from app.Database.Postgres_connection_engine import engine
from sqlmodel import  SQLModel
from .routers import authentication, dictionary

SQLModel.metadata.create_all(engine)

app = FastAPI()


app.include_router(authentication.router)
app.include_router(dictionary.router)

@app.get("/")
async def root():
    return "hello"




