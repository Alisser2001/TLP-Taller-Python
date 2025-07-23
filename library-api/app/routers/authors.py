from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import Author, AuthorCreate, AuthorUpdate, Message
from app.services.author_service import AuthorService
from typing import List

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Author])
def get_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = AuthorService.get_authors(db, skip=skip, limit=limit)
    return authors

@router.get("/{author_id}", response_model=Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = AuthorService.get_author(db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.post("/", response_model=Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    try:
        return AuthorService.create_author(db=db, author=author)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{author_id}", response_model=Author)
def update_author(author_id: int, author_update: AuthorUpdate, db: Session = Depends(get_db)):
    try:
        author = AuthorService.update_author(db, author_id, author_update)
        if author is None:
            raise HTTPException(status_code=404, detail="Author not found")
        return author
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{author_id}", response_model=Message)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    try:
        success = AuthorService.delete_author(db, author_id)
        if not success:
            raise HTTPException(status_code=404, detail="Author not found")
        return {"message": "Author deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))