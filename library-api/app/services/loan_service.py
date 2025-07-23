from sqlalchemy.orm import Session
from app.models.models import Loan, Book
from app.schemas.schemas import LoanCreate
from datetime import datetime
from typing import List, Optional


class LoanService:
    @staticmethod
    def get_loans(db: Session, skip: int = 0, limit: int = 100) -> List[Loan]:
        return db.query(Loan).offset(skip).limit(limit).all()

    @staticmethod
    def get_loan(db: Session, loan_id: int) -> Optional[Loan]:
        return db.query(Loan).filter(Loan.id == loan_id).first()

    @staticmethod
    def create_loan(db: Session, loan: LoanCreate) -> Loan:
        book = db.query(Book).filter(Book.id == loan.book_id).first()
        if not book:
            raise ValueError("Book not found")
        if not book.available:
            raise ValueError("Book is not available for loan")
        db_loan = Loan(**loan.dict())
        db.add(db_loan)
        book.available = False
        db.commit()
        db.refresh(db_loan)
        return db_loan

    @staticmethod
    def return_book(db: Session, loan_id: int) -> Optional[Loan]:
        db_loan = LoanService.get_loan(db, loan_id)
        if not db_loan:
            return None
        if db_loan.returned:
            raise ValueError("Book already returned")
        db_loan.returned = True
        db_loan.return_date = datetime.utcnow()
        db_loan.book.available = True
        db.commit()
        db.refresh(db_loan)
        return db_loan

    @staticmethod
    def get_active_loans(db: Session) -> List[Loan]:
        return db.query(Loan).filter(Loan.returned == False).all()

    @staticmethod
    def get_loans_by_user(db: Session, user_email: str) -> List[Loan]:
        return db.query(Loan).filter(Loan.user_email == user_email).all()

    @staticmethod
    def delete_loan(db: Session, loan_id: int) -> bool:
        db_loan = LoanService.get_loan(db, loan_id)
        if not db_loan:
            return False
        if not db_loan.returned:
            db_loan.book.available = True
        db.delete(db_loan)
        db.commit()
        return True