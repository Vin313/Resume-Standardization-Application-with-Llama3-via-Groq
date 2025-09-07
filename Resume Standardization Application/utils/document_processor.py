import pdfplumber
import docx2txt
import re
from typing import Dict, Any
import PyPDF2
import io

class DocumentProcessor:
    @staticmethod
    def extract_text_from_pdf(file_content) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            # Try with pdfplumber first for better table extraction
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            
            # Fallback to PyPDF2 if pdfplumber doesn't extract enough text
            if len(text.strip()) < 100:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
        
        return text.strip()

    @staticmethod
    def extract_text_from_docx(file_content) -> str:
        """Extract text from DOCX file"""
        try:
            text = docx2txt.process(io.BytesIO(file_content))
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")

    @staticmethod
    def extract_text_from_file(file_content, file_type: str) -> str:
        """Extract text based on file type"""
        if file_type == "application/pdf":
            return DocumentProcessor.extract_text_from_pdf(file_content)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return DocumentProcessor.extract_text_from_docx(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    @staticmethod
    def preprocess_text(text: str) -> str:
        """Clean and preprocess extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\-\:\;\(\)\@]', '', text)
        return text.strip()