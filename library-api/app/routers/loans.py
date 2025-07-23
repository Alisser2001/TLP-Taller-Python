from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import Loan, LoanCreate, Message
from app.services.loan_service import LoanService
from typing import List

router = APIRouter(
    prefix="/loans",
    tags=["loans"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Loan])
def get_loans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    loans = LoanService.get_loans(db, skip=skip, limit=limit)
    return loans

@router.get("/active", response_model=List[Loan])
def get_active_loans(db: Session = Depends(get_db)):
    loans = LoanService.get_active_loans(db)
    return loans

@router.get("/user/{user_email}", response_model=List[Loan])
def get_loans_by_user(user_email: str, db: Session = Depends(get_db)):
    loans = LoanService.get_loans_by_user(db, user_email)
    return loans

@router.get("/{loan_id}", response_model=Loan)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = LoanService.get_loan(db, loan_id=loan_id)
    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

@router.post("/", response_model=Loan)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    try:
        return LoanService.create_loan(db=db, loan=loan)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{loan_id}/return", response_model=Loan)
def return_book(loan_id: int, db: Session = Depends(get_db)):
    try:
        loan = LoanService.return_book(db, loan_id)
        if loan is None:
            raise HTTPException(status_code=404, detail="Loan not found")
        return loan
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{loan_id}", response_model=Message)
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    try:
        success = LoanService.delete_loan(db, loan_id)
        if not success:
            raise HTTPException(status_code=404, detail="Loan not found")
        return {"message": "Loan deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))