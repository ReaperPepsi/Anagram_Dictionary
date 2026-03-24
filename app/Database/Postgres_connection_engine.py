from sqlmodel import create_engine, Session
from typing import Annotated
from fastapi.params import Depends
from app.utils.db_connection_string import DATABASE_URL


#conexiunea propriu-zisa
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    # Deschide o sesiune SQLAlchemy pentru fiecare request
    with Session(engine) as session:
        # yield permite FastAPI să injecteze session-ul în route
        # după ce request-ul se termină, session-ul se închide automat
        yield session


SessionDep = Annotated[Session, Depends(get_session)]



