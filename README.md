# Resume-Standardization-Application-with-Llama3-via-Groq
Resume Standardization Application with Llama3 via Groq API

A Generative AI-powered application that converts resumes in various formats (PDF/DOCX) into a standardized format using Llama3 through Groq API.
<img width="1920" height="890" alt="image" src="https://github.com/user-attachments/assets/2eafc068-a62f-40ba-9ffc-2e7bcdbe8667" />


# Features
### Multi-format Support: Processes both PDF and DOCX resume files

### AI-Powered Extraction: Uses Llama3 model to accurately extract resume information

### Standardized Formatting: Converts resumes to a consistent, professional format

### Tone Customization: Allows specifying tone guidelines for the output resume

### Editable Output: Generates downloadable DOCX files for further editing

### User-Friendly Interface: Streamlit-based web UI for easy interaction

# Prerequisites
Before running this application, you need:

Python 3.8+ is installed on your system

Groq API Account with access to Llama3 models

API Key from Groq (available at console.groq.com)

# Installation
Clone or download the project files to your local machine

Navigate to the project directory:

bash
Install required dependencies:

bash
pip install -r requirements.txt
Set up environment variables:

Create a .env file in the project root directory

Add your Groq API key:

text
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama3-70b-8192
LLM_PROVIDER=groq
Usage
Start the application:

bash
streamlit run main.py
Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

# Use the application:

Upload your resume file (PDF or DOCX format)

Optionally specify tone guidelines (e.g., "formal", "technical focus", etc.)

Select your preferred Llama3 model variant

Click "Process Resume"

Review the extracted information

Download the standardized resume in DOCX format
