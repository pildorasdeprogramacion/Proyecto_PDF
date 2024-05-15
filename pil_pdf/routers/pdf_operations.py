from fastapi import APIRouter, UploadFile, File, HTTPException
from pypdf  import PdfReader, PdfWriter
from starlette.responses import Response
from pdf2docx import Converter
import io

router = APIRouter()

MAX_FILE_SIZE = 7 * 1024 * 1024
MAX_FILE_SIZE_MERGE = 20 * 1024 * 1024

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

    writer_pdf.encrypt(user_password=pwd, use_128bit=True)

    protected_pdf_buffer = io.BytesIO()
    writer_pdf.write(protected_pdf_buffer)
    protected_pdf_buffer.seek(0)

    content = protected_pdf_buffer.getvalue()
    headers = {
        "Content-Disposition": "attachment; filename=protected.pdf"
    }
    return Response(content=content, media_type="application/pdf", headers=headers)

@router.post("/merge-pdfs/")
async def merge_pdfs(files: list[UploadFile] = File(...)):
    if len(files) < 2:
        raise HTTPException(status_code=400, 
                detail="At least two PDF files are required to merge")
    if sum([file.size for file in files]) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413,
                detail="Total file size exceeds the maximum allowed limit")

    writer_pdf = PdfWriter()

    for file in files:
        try:
            reader_pdf = PdfReader(file.file)
        except Exception:
            raise HTTPException(status_code=400, 
                    detail="The uploaded file is not a valid PDF")

        for page in reader_pdf.pages:
            writer_pdf.add_page(page)

    merged_pdf_buffer = io.BytesIO()
    writer_pdf.write(merged_pdf_buffer)
    merged_pdf_buffer.seek(0)

    content = merged_pdf_buffer.getvalue()
    headers = {
        "Content-Disposition": "attachment; filename=merged.pdf"
    }
    return Response(content=content, 
                    media_type="application/pdf", 
                    headers=headers)

@router.post("/remove-password/")
async def remove_password(file: UploadFile = File(...), 
                          pwd: str = ""):
    if not pwd:
        raise HTTPException(status_code=400, 
            detail="pwd is required")
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, 
            detail="File size exceeds the\
                  maximum allowed limit")
    try:
        reader_pdf = PdfReader(file.file)
        if reader_pdf.is_encrypted:
            reader_pdf.decrypt(pwd)
    except Exception:
        raise HTTPException(status_code=400, 
                detail="The uploaded file is not a\
             valid PDF or password is incorrect")

    writer_pdf = PdfWriter(clone_from=reader_pdf)

    pdf_buffer = io.BytesIO()
    writer_pdf.write(pdf_buffer)
    pdf_buffer.seek(0)

    content = pdf_buffer.getvalue()
    headers = {
        "Content-Disposition": "attachment; \
            filename=unlocked.pdf"
    }
    return Response(content=content, 
                    media_type="application/pdf", 
                    headers=headers)

@router.post("/pdf-to-word/")
async def pdf_to_word(file: UploadFile = File(...)):
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, 
            detail="File size exceeds the\
                  maximum allowed limit")
    try:
        pdf_content = await file.read() 
    except Exception:
        raise HTTPException(status_code=400, 
            detail="The uploaded file is \
                not a valid PDF")
    
    docx_buffer = io.BytesIO()

    try:
        converter = Converter(stream=pdf_content)
        converter.convert(docx_buffer)
        converter.close()
    except Exception as e:
        raise HTTPException(status_code=500, 
            detail=f"Error converting PDF to Word: {e}")
    
    docx_buffer.seek(0)
    headers = {
        "Content-Disposition": "attachment; \
            filename=converted.docx"
    }
    return Response(content=docx_buffer.getvalue(), 
            media_type="application/vnd.openxml\
                formats-officedocument.\
                wordprocessingml.document", 
            headers=headers)
    

    





