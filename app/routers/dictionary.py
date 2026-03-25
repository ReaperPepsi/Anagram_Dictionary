from fastapi import HTTPException, status, Response, APIRouter, Depends
from app.Database.Postgres_connection_engine import SessionDep
from app.utils.oath2 import get_current_user
from app.Models.Anagram_Dictionary_Models import AnagramInput, AnagramDictionary, AnagramPostResponse, AnagramGroup
from sqlmodel import select
from sqlalchemy.exc import IntegrityError


router = APIRouter(
    prefix = "/words",
    tags=["Anagrams"]
)

def sort_word(word: str) -> str:
    return "".join(sorted(word))


@router.post("/", response_model= AnagramPostResponse, status_code=status.HTTP_201_CREATED)
def group_anagrams(words: AnagramInput, session: SessionDep, current_user: int = Depends(get_current_user)):
    list_of_added = []
    list_of_skipped = []

    for current_word in words.words:
        if not current_word:
            list_of_skipped.append({
                "word": current_word,
                "reason": "emtpy word provided"
            })
            continue

        new_word = AnagramDictionary(
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




@router.get('/list', response_model=list[AnagramGroup])
def get_all_groups(session: SessionDep, current_user: int = Depends(get_current_user)):
    data_from_db = session.exec(select(AnagramDictionary).where(AnagramDictionary.user_id == current_user.id)).all()

    if not data_from_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Your user do not have any post")

    response = dict()
    for data in data_from_db:
        if data.key_word not in response:
            response[data.key_word] = [data.word]
        else:
            response[data.key_word].append(data.word)

    return [AnagramGroup(key_word=k, words=v) for k, v in response.items()]




@router.get("/list/{word}", response_model=list[AnagramGroup])
def get_word_anagram_group(word: str, session: SessionDep, current_user: int = Depends(get_current_user)):
    key_word_from_db = session.exec(select(AnagramDictionary.key_word).where(AnagramDictionary.user_id == current_user.id, AnagramDictionary.key_word == sort_word(word))).first()

    if not key_word_from_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Your do not have any anagram dictionary for this word")
    
    data_from_db = session.exec(select(AnagramDictionary).where(AnagramDictionary.user_id == current_user.id, AnagramDictionary.key_word == key_word_from_db)).all()

    words_list = [item.word for item in data_from_db]
    return [AnagramGroup(key_word=key_word_from_db, words=words_list)]