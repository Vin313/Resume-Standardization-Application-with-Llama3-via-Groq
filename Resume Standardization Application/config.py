import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # "groq" for Llama3
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "llama3-70b-8192")
    
    # Processing settings
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    SUPPORTED_FORMATS = [".pdf", ".docx"]
    
    # Output settings
    DEFAULT_OUTPUT_FILENAME = "standardized_resume.docx"
    
    # Cost control
    MAX_TOKENS = 4000
    TEMPERATURE = 0.1
    MAX_RETRIES = 3
    