from fastapi import HTTPException, status, Response, APIRouter, Depends
from app.Database.Postgres_connection_engine import SessionDep
from app.utils.oath2 import get_current_user
from app.Models.Anagram_Dictionary_Models import Anagram_Input, Anagram_Dictionary, Anagram_Response
from sqlmodel import select
from sqlalchemy.exc import IntegrityError


router = APIRouter(
    prefix = "/words",
    tags=["Anagrams"]
)

def sort_word(word: str) -> str:
    return "".join(sorted(word))




@router.post("/", response_model= Anagram_Response, status_code=status.HTTP_201_CREATED)
def group_anagrams(words: Anagram_Input, session: SessionDep, current_user: int = Depends(get_current_user)):
    list_of_added = []
    list_of_skipped = []

    for current_word in words.words:
        if not current_word:
            list_of_skipped.append({
                "word": current_word,
                "reason": "emtpy word provided"
            })
            continue

        new_word = Anagram_Dictionary(
        word=current_word,
        key_word=sort_word(current_word),
        user_id=current_user.id
        ) 

        try:
            session.add(new_word)
            session.commit()
            session.refresh(new_word)
            list_of_added.append(new_word.word)

        except IntegrityError as e:
            session.rollback()
            
            if isinstance(e.orig, Exception) and hasattr(e.orig, "sqlstate"):
                if e.orig.sqlstate == "23505":
                    reason = "duplicate_value"
                else:
                    reason = "db_constraint_error"
            else:
                reason = "unknown_error"

            list_of_skipped.append({
                "word": current_word,
                "reason": reason
            })

    return {"added": list_of_added, "skipped" : list_of_skipped}