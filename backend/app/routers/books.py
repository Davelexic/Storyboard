from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select

from ..db import get_session
from ..models import Book, User
from ..security import get_current_user
from ..services.parser import parse_epub
from ..services.converter import generate_cinematic_markup
import os
import tempfile

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/upload")
async def upload_book(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if file.content_type != "application/epub+zip":
        raise HTTPException(status_code=400, detail="Invalid file type")
    try:
        contents = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        parsed_book = parse_epub(tmp_path)
        markup = generate_cinematic_markup(parsed_book)

        book = Book(
            title=parsed_book.get("title", file.filename),
            owner_id=current_user.id,
            markup=markup,
        )
        session.add(book)
        session.commit()
        session.refresh(book)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to process EPUB file") from e
    finally:
        if "tmp_path" in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)

    return markup


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


@router.get("/{book_id}/markup")
def read_book_markup(
    book_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    book = session.get(Book, book_id)
    if not book or book.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.markup is None:
        raise HTTPException(status_code=404, detail="Markup not found")
    return book.markup
