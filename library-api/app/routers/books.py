from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import Book, BookCreate, BookUpdate, BookDiscount, Message
from app.services.book_service import BookService
from typing import List

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Book])
def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = BookService.get_books(db, skip=skip, limit=limit)
    return books

@router.get("/available", response_model=List[Book])
def get_available_books(db: Session = Depends(get_db)):
    books = BookService.get_available_books(db)
    return books

@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = BookService.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    try:
        return BookService.create_book(db=db, book=book)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    try:
        book = BookService.update_book(db, book_id, book_update)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return book
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{book_id}", response_model=Message)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    try:
        success = BookService.delete_book(db, book_id)
        if not success:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"message": "Book deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{book_id}/discount", response_model=Book)
def apply_discount(book_id: int, discount: BookDiscount, db: Session = Depends(get_db)):
    try:
        book = BookService.apply_discount(db, book_id, discount.discount_percentage)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found or has no price")
        return book
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))