from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class AuthorBase(BaseModel):
    name: str
    nationality: Optional[str] = None
    birth_year: Optional[int] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    nationality: Optional[str] = None
    birth_year: Optional[int] = None

class Author(AuthorBase):
    id: int
    class Config:
        from_attributes = True

class BookBase(BaseModel):
    title: str
    isbn: str
    pages: Optional[int] = None
    price: Optional[float] = None
    author_id: int

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    pages: Optional[int] = None
    price: Optional[float] = None
    author_id: Optional[int] = None
    available: Optional[bool] = None

class Book(BookBase):
    id: int
    available: bool
    author: Author
    class Config:
        from_attributes = True

class LoanBase(BaseModel):
    user_name: str
    user_email: str
    book_id: int

class LoanCreate(LoanBase):
    pass

class LoanReturn(BaseModel):
    returned: bool = True

class Loan(LoanBase):
    id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    returned: bool
    book: Book
    class Config:
        from_attributes = True

class BookDiscount(BaseModel):
    discount_percentage: float

class Message(BaseModel):
    message: str