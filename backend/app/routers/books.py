from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..db import get_session
from ..models import Book

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=Book)
def create_book(book: Book, session: Session = Depends(get_session)):
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.get("/", response_model=list[Book])
def read_books(session: Session = Depends(get_session)):
    return session.exec(select(Book)).all()


@router.get("/{book_id}", response_model=Book)
def read_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
