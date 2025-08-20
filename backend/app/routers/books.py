from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..db import get_session
from ..models import Book, User
from ..security import get_current_user

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=Book)
def create_book(
    book: Book,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    book.owner_id = current_user.id
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.get("/", response_model=list[Book])
def read_books(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return session.exec(select(Book).where(Book.owner_id == current_user.id)).all()


@router.get("/{book_id}", response_model=Book)
def read_book(
    book_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    book = session.get(Book, book_id)
    if not book or book.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
