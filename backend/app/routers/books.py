from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlmodel import Session, select
from typing import List
import os
import tempfile
from datetime import datetime

from ..db import get_session
from ..models import Book, User
from ..middleware.auth import get_current_user
from ..services.parser import parse_epub
from ..services.story_analyzer import StoryAnalyzer
from ..config import settings
from ..utils.sanitization import sanitize_filename, SanitizationError
from ..exceptions import (
    ValidationError,
    FileProcessingError,
    BookProcessingError,
    ResourceNotFoundError,
    DatabaseError
)

router = APIRouter(prefix="/books", tags=["books"])

story_analyzer = StoryAnalyzer()


def process_book_background(book_id: int, file_path: str, session: Session):
    """Background task to process book analysis."""
    try:
        # Update status to processing
        book = session.get(Book, book_id)
        if book:
            book.processing_status = "processing"
            book.updated_at = datetime.utcnow()
            session.commit()
        
        # Parse EPUB
        parsed_book = parse_epub(file_path)
        
        # Run analysis
        markup = story_analyzer.analyze_and_enhance(parsed_book)
        
        # Update book with results
        book = session.get(Book, book_id)
        if book:
            book.markup = markup
            book.processing_status = "completed"
            book.processed_at = datetime.utcnow()
            book.theme = markup.get('theme', 'general')
            book.total_chapters = len(markup.get('chapters', []))
            
            # Calculate effect statistics
            total_effects = 0
            for chapter in markup.get('chapters', []):
                for content in chapter.get('content', []):
                    total_effects += len(content.get('effects', []))
            
            book.total_effects = total_effects
            book.effect_density = total_effects / max(1, book.total_chapters)
            
            session.commit()
            
    except Exception as e:
        # Update status to failed
        book = session.get(Book, book_id)
        if book:
            book.processing_status = "failed"
            book.processing_error = str(e)
            book.updated_at = datetime.utcnow()
            session.commit()


@router.post("/upload")
async def upload_book(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Upload and process an EPUB file."""
    
    # Sanitize filename
    try:
        if file.filename:
            sanitized_filename = sanitize_filename(file.filename)
        else:
            raise ValidationError("No filename provided", field="filename")
    except SanitizationError as e:
        raise ValidationError(f"Invalid filename: {str(e)}", field="filename")
    
    # Validate file type
    if not sanitized_filename.lower().endswith('.epub'):
        raise FileProcessingError("Only EPUB files are supported", file_type="epub")
    
    # Validate file size
    if file.size and file.size > settings.max_file_size:
        raise FileProcessingError(
            f"File size exceeds maximum limit of {settings.max_file_size // (1024*1024)}MB",
            file_type="epub"
        )
    
    try:
        # Read file content
        contents = await file.read()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name
        
        # Parse basic metadata first
        try:
            parsed_book = parse_epub(tmp_path)
        except Exception as e:
            os.unlink(tmp_path)
            raise FileProcessingError(f"Invalid EPUB file: {str(e)}", file_type="epub")
        
        # Create book record with sanitized data
        book = Book(
            title=parsed_book.get("title", sanitized_filename),
            author=parsed_book.get("author", "Unknown Author"),
            language=parsed_book.get("language", "en"),
            identifier=parsed_book.get("identifier"),
            owner_id=current_user.id,
            file_size=len(contents),
            file_path=tmp_path,
            processing_status="pending",
            total_chapters=parsed_book.get("total_chapters", 0),
            book_metadata=parsed_book.get("parsing_metadata", {})
        )
        
        session.add(book)
        session.commit()
        session.refresh(book)
        
        # Start background processing
        background_tasks.add_task(process_book_background, book.id, tmp_path, session)
        
        return {
            "job_id": book.id,
            "status": "pending",
            "message": "Book uploaded successfully. Processing started in background."
        }
        
    except (HTTPException, CineiReaderException):
        raise
    except Exception as e:
        # Clean up temporary file if it exists
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise BookProcessingError(f"Failed to process EPUB file: {str(e)}")


@router.get("/jobs/{job_id}/status")
def get_job_status(
    job_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get the status of a book processing job."""
    book = session.get(Book, job_id)
    if not book or book.owner_id != current_user.id:
        raise ResourceNotFoundError("Job not found", resource_type="job", resource_id=str(job_id))
    
    return {
        "job_id": job_id,
        "status": book.processing_status,
        "error": book.processing_error,
        "created_at": book.created_at,
        "updated_at": book.updated_at,
        "processed_at": book.processed_at
    }


@router.get("/jobs/{job_id}/result")
def get_job_result(
    job_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get the processed markup result."""
    book = session.get(Book, job_id)
    if not book or book.owner_id != current_user.id:
        raise ResourceNotFoundError("Job not found", resource_type="job", resource_id=str(job_id))
    
    if book.processing_status != "completed":
        raise BookProcessingError(
            f"Job not completed. Current status: {book.processing_status}",
            book_id=job_id
        )
    
    if book.markup is None:
        raise ResourceNotFoundError("Result not available", resource_type="markup", resource_id=str(job_id))
    
    return book.markup


@router.get("/", response_model=List[Book])
def read_books(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get all books for the current user."""
    return session.exec(
        select(Book)
        .where(Book.owner_id == current_user.id)
        .order_by(Book.created_at.desc())
    ).all()


@router.get("/{book_id}", response_model=Book)
def read_book(
    book_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get a specific book by ID."""
    book = session.get(Book, book_id)
    if not book or book.owner_id != current_user.id:
        raise ResourceNotFoundError("Book not found", resource_type="book", resource_id=str(book_id))
    return book


@router.get("/{book_id}/markup")
def read_book_markup(
    book_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get the processed markup for a book."""
    book = session.get(Book, book_id)
    if not book or book.owner_id != current_user.id:
        raise ResourceNotFoundError("Book not found", resource_type="book", resource_id=str(book_id))
    
    if book.processing_status != "completed":
        raise BookProcessingError(
            f"Book not fully processed. Status: {book.processing_status}",
            book_id=book_id
        )
    
    if book.markup is None:
        raise ResourceNotFoundError("Markup not found", resource_type="markup", resource_id=str(book_id))
    
    return book.markup


@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Delete a book and its associated files."""
    book = session.get(Book, book_id)
    if not book or book.owner_id != current_user.id:
        raise ResourceNotFoundError("Book not found", resource_type="book", resource_id=str(book_id))
    
    try:
        # Delete associated file if it exists
        if book.file_path and os.path.exists(book.file_path):
            os.unlink(book.file_path)
        
        # Delete from database
        session.delete(book)
        session.commit()
        
        return {"message": "Book deleted successfully"}
        
    except Exception as e:
        raise DatabaseError(f"Failed to delete book: {str(e)}", operation="delete")
