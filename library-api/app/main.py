from fastapi import FastAPI
from app.database import create_tables
from app.routers import books, authors, loans

create_tables()

app = FastAPI(
    title="Biblioteca API",
    description="API para gestión de biblioteca con libros, autores y préstamos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(authors.router)
app.include_router(books.router)
app.include_router(loans.router)

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a la API de Biblioteca",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}