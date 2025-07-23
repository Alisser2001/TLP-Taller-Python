from sqlalchemy.orm import Session
from app.models.models import Book, Author
from app.schemas.schemas import BookCreate, BookUpdate
from typing import List, Optional

class BookService:
    @staticmethod
    def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[Book]:
        return db.query(Book).offset(skip).limit(limit).all()

    @staticmethod
    def get_book(db: Session, book_id: int) -> Optional[Book]:
        return db.query(Book).filter(Book.id == book_id).first()

    @staticmethod
    def get_book_by_isbn(db: Session, isbn: str) -> Optional[Book]:
        return db.query(Book).filter(Book.isbn == isbn).first()

    @staticmethod
    def create_book(db: Session, book: BookCreate) -> Book:
        author = db.query(Author).filter(Author.id == book.author_id).first()
        if not author:
            raise ValueError("Author not found")
        existing_book = BookService.get_book_by_isbn(db, book.isbn)
        if existing_book:
            raise ValueError("Book with this ISBN already exists")
        db_book = Book(**book.dict())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    @staticmethod
    def update_book(db: Session, book_id: int, book_update: BookUpdate) -> Optional[Book]:
        db_book = BookService.get_book(db, book_id)
        if not db_book:
            return None
        update_data = book_update.dict(exclude_unset=True)
        if "author_id" in update_data:
            author = db.query(Author).filter(Author.id == update_data["author_id"]).first()
            if not author:
                raise ValueError("Author not found")
        if "isbn" in update_data:
            existing_book = BookService.get_book_by_isbn(db, update_data["isbn"])
            if existing_book and existing_book.id != book_id:
                raise ValueError("Book with this ISBN already exists")
        for field, value in update_data.items():
            setattr(db_book, field, value)
        db.commit()
        db.refresh(db_book)
        return db_book

    @staticmethod
    def delete_book(db: Session, book_id: int) -> bool:
        db_book = BookService.get_book(db, book_id)
        if not db_book:
            return False
        active_loans = any(not loan.returned for loan in db_book.loans)
        if active_loans:
            raise ValueError("Cannot delete book with active loans")
        db.delete(db_book)
        db.commit()
        return True

    @staticmethod
    def apply_discount(db: Session, book_id: int, discount_percentage: float) -> Optional[Book]:
        db_book = BookService.get_book(db, book_id)
        if not db_book or not db_book.price:
            return None
        if discount_percentage < 0 or discount_percentage > 100:
            raise ValueError("Discount percentage must be between 0 and 100")
        new_price = db_book.price * (1 - discount_percentage / 100)
        db_book.price = round(new_price, 2)
        db.commit()
        db.refresh(db_book)
        return db_book

    @staticmethod
    def get_available_books(db: Session) -> List[Book]:
        return db.query(Book).filter(Book.available == True).all()