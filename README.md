
# PIL_PDF

This is a [FastAPI](https://fastapi.tiangolo.com/)-based project that provides services for working with PDF files. Currently, it offers a function to protect PDF files with a password. As the project evolves, more PDF-related functions may be added.

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

## Project Structure

- **/Proyecto_PDF/**: Project root directory.
- **/pil_pdf/**: Directory containing code related to PDF operations.
    - **/__init__.py**: File that marks the directory as a Python package.
    - **/main.py**: File containing initialization and configuration of the FastAPI application.
    - **/routers/**: Directory containing FastAPI routers for defining API routes.
        - **/__init__.py**: File that marks the directory as a Python package.
        - **/pdf_operations.py**: File containing routes related to PDF operations.
- **requirements.txt**: File containing project dependencies.
- **README.md**: This file, providing information about the project.
- **.gitignore**: Configuration file for ignoring unwanted files in version control.

## Dependencies

Project dependencies are defined in the `requirements.txt` file. You can install them using the following command:

```bash
pip install -r requirements.txt
```
## Running the Project

To run the project, ensure you have a configured Python environment. Then, run the main.py file in the project root directory using the following command:

```bash
uvicorn pil_pdf.main:app --reload
```
This will start a development server that will automatically reload when code changes are detected.

## Usage
### Protecting a PDF with a Password
The project currently offers one endpoint to protect PDF files with a password:

**POST /protect-pdf/**
You can send a POST request to this endpoint with a PDF file and a password in the body of the request. If the file and password are valid, the server will return the protected PDF file.

Example request:

- Using the FastAPI interactive API documentation at http://localhost:8000/docs, navigate to the /protect-pdf/ endpoint.
- Upload a PDF file and specify the password you want to use to protect the file.
- Submit the request and you will receive the protected PDF file in response.

Alternatively, you can use curl:

```bash
curl -X POST "http://localhost:8000/protect-pdf/" \
    -F "file=@/path/to/file.pdf" \
    -F "pwd=secret_password"
```
This will send a PDF file to the server and receive the protected PDF file as a response.

## Contributions
This project is open to contributions. If you have ideas for new features or improvements, feel free to open an issue or submit a pull request.
