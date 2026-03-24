from fastapi import FastAPI
from app.Database.Postgres_connection_engine import SessionDep
from sqlmodel import select
from sqlalchemy import text

app = FastAPI()

@app.get("/")
async def root():
    return "hello"


@app.get("/test")
async def get_test_values(session: SessionDep):
    result = session.execute(text("SELECT * FROM test"))
    rows = result.fetchall()  # tuple list
    
    # Convertim la listă de dicturi pentru JSON
    data = [dict(row._mapping) for row in rows]
    return data
    



