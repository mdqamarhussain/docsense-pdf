from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, File, HTTPException, UploadFile
from app.schemas.upload import UploadResponse
from app.services.document_processor import process_pdf


router = APIRouter(
    prefix="/upload",
    tags=["upload"],
)

UPLOAD_DIR = Path("uploads") 


@router.post("/", response_model=UploadResponse)
def upload_pdf(file: UploadFile = File(...)):
    filename = file.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Only PDF files are supported")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_path = UPLOAD_DIR / f"{uuid4().hex}.pdf"

    try:
        return process_pdf(file, file_path)
    finally:
        file.file.close()
        file_path.unlink(missing_ok=True)