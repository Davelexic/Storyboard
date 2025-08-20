from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/upload")
async def upload_book(file: UploadFile = File(...)):
    """Placeholder endpoint for uploading an EPUB file."""
    # TODO: Save file and trigger conversion engine
    return {"filename": file.filename, "status": "processing"}
