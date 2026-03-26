from sqlmodel import create_engine, Session
from typing import Annotated
from fastapi.params import Depends
from app.utils.db_connection_string import DATABASE_URL


# create the engine to hold up the sessions
engine = create_engine(DATABASE_URL, echo=True)


# use get_session() as a Dependecy injection for each relevant endpoint
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]



