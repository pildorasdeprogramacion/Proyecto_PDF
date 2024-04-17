from fastapi import APIRouter, UploadFile, File, HTTPException
from PyPDF2 import PdfReader, PdfWriter
from starlette.responses import Response
import io

router = APIRouter()

MAX_FILE_SIZE = 7 * 1024 * 1024

@router.post("/protect-pdf/")
async def protect_pdf(file: UploadFile = File(...), pwd: str = ""):

    if not pwd:
        raise HTTPException(status_code=400, detail="pwd is required")
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File size exceeds the maximum allowed limit")
    try:
        reader_pdf = PdfReader(file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid PDF")

    writer_pdf = PdfWriter()

    for page in reader_pdf.pages:
        writer_pdf.add_page(page)

    writer_pdf.encrypt(user_password=pwd, owner_pwd=None, use_128bit=True)

    protected_pdf_buffer = io.BytesIO()
    writer_pdf.write(protected_pdf_buffer)
    protected_pdf_buffer.seek(0)

    content = protected_pdf_buffer.getvalue()
    headers = {
        "Content-Disposition": "attachment; filename=protected.pdf"
    }
    return Response(content=content, media_type="application/pdf", headers=headers)
