from fastapi import FastAPI
from app.logging_config import setup_logging
from app.Database.Postgres_connection_engine import engine
from sqlmodel import  SQLModel
from .routers import authentication, dictionary


setup_logging()


# create all tables inside Models folder at startup (if not created)
SQLModel.metadata.create_all(engine)

app = FastAPI()

# add created router for the specific endpoints
app.include_router(authentication.router)
app.include_router(dictionary.router)


# define the root endpoint
@app.get("/")
async def root():
    return {"message": "this is the root page"}




