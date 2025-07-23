from sqlalchemy.orm import Session
from app.models.models import Author
from app.schemas.schemas import AuthorCreate, AuthorUpdate
from typing import List, Optional

class AuthorService:
    @staticmethod
    def get_authors(db: Session, skip: int = 0, limit: int = 100) -> List[Author]:
        return db.query(Author).offset(skip).limit(limit).all()

    @staticmethod
    def get_author(db: Session, author_id: int) -> Optional[Author]:
        return db.query(Author).filter(Author.id == author_id).first()

    @staticmethod
    def create_author(db: Session, author: AuthorCreate) -> Author:
        db_author = Author(**author.dict())
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
        return db_author

    @staticmethod
    def update_author(db: Session, author_id: int, author_update: AuthorUpdate) -> Optional[Author]:
        db_author = AuthorService.get_author(db, author_id)
        if not db_author:
            return None
        update_data = author_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_author, field, value)
        db.commit()
        db.refresh(db_author)
        return db_author

    @staticmethod
    def delete_author(db: Session, author_id: int) -> bool:
        db_author = AuthorService.get_author(db, author_id)
        if not db_author:
            return False
        if db_author.books:
            raise ValueError("Cannot delete author with associated books")
        db.delete(db_author)
        db.commit()
        return True