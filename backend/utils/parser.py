import pdfplumber
from docx import Document
import io


def parse_resume(file: io.BytesIO, filename: str) -> str:
    """
    Parses the content of a resume file (PDF or DOCX).
    """
    text = ""
    if filename.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif filename.endswith(".docx"):
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX file.")

    return text