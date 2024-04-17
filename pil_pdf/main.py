from fastapi import FastAPI
from .routers import pdf_operations

app = FastAPI()

app.include_router(pdf_operations.router)

