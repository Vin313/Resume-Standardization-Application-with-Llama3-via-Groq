import streamlit as st
import tempfile
import os
from utils.document_processor import DocumentProcessor
from utils.llm_integration import LLMIntegration
from utils.docx_generator import DocxGenerator
import config
import time
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Resume Standardizer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None
if 'output_file' not in st.session_state:
    st.session_state.output_file = None

def process_resume(uploaded_file, tone_guidelines):
    """Process the uploaded resume file"""
    try:
        # Read file content
        file_content = uploaded_file.read()
        
        # Extract text
        processor = DocumentProcessor()
        text = processor.extract_text_from_file(file_content, uploaded_file.type)
        preprocessed_text = processor.preprocess_text(text)
        
        # Extract information using LLM
        llm = LLMIntegration()
        resume_data = llm.extract_resume_info(preprocessed_text, tone_guidelines)
        
        # Refine content if tone guidelines are provided
        if tone_guidelines:
            resume_data = llm.refine_content(resume_data, tone_guidelines)
        
        # Generate standardized document
        doc_generator = DocxGenerator()
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
            doc_generator.save_document(resume_data, tmp_file.name)
            
            # Read the file content for download
            with open(tmp_file.name, 'rb') as f:
                output_content = f.read()
            
            # Clean up
            os.unlink(tmp_file.name)
        
        return resume_data, output_content, None
        
    except Exception as e:
        return None, None, str(e)

# UI Components
st.title("📄 Resume Standardization Tool")
st.markdown("Upload your resume in PDF or DOCX format to convert it to our standardized format.")

# Sidebar for additional options
with st.sidebar:
    st.header("Options")
    
    # Model selection
    model_option = st.selectbox(
        "Select Model",
        ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"],
        help="Select the Llama3 model variant to use for processing"
    )
    
    # Update config with selected model
    config.Config.MODEL_NAME = model_option
    
    tone_guidelines = st.text_area(
        "Tone Guidelines (Optional)",
        height=100,
        help="Provide instructions for tone (e.g., 'Use formal language', 'Focus on technical skills', etc.)"
    )
    
    st.info("""
    **How it works:**
    1. Upload your resume (PDF or DOCX)
    2. AI extracts and structures your information using Llama3
    3. Download your standardized resume
    """)
    
    # API key input (for flexibility)
    api_key = st.text_input(
        "Groq API Key (Optional)",
        type="password",
        help="If not set in environment variables, enter your Groq API key here"
    )
    
    if api_key:
        config.Config.GROQ_API_KEY = api_key

# File upload
uploaded_file = st.file_uploader(
    "Choose a resume file",
    type=['pdf', 'docx'],
    help="Supported formats: PDF, DOCX"
)

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original File Preview")
        if uploaded_file.type == "application/pdf":
            st.warning("PDF preview not available. Processing will still work.")
        else:
            st.info("File uploaded successfully. Click process to continue.")
    
    with col2:
        st.subheader("Processing")
        
        if st.button("Process Resume", type="primary"):
            with st.spinner("Processing your resume with Llama3..."):
                start_time = time.time()
                
                resume_data, output_content, error = process_resume(uploaded_file, tone_guidelines)
                
                processing_time = time.time() - start_time
                
                if error:
                    st.error(f"Error processing resume: {error}")
                else:
                    st.session_state.resume_data = resume_data
                    st.session_state.output_file = output_content
                    st.session_state.processing_time = processing_time
                    st.session_state.processed = True
                    
                    st.success("Resume processed successfully!")

# Display results if processing is complete
if st.session_state.processed and st.session_state.resume_data:
    st.divider()
    st.subheader("Processed Resume Data")
    
    # Show extracted information
    with st.expander("View Extracted Information"):
        st.json(st.session_state.resume_data)
    
    # Show processing stats
    st.metric("Processing Time", f"{st.session_state.processing_time:.2f} seconds")
    
    # Download button
    st.download_button(
        label="Download Standardized Resume",
        data=st.session_state.output_file,
        file_name="standardized_resume.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        icon="📥"
    )

# Footer
st.divider()
st.caption("""
This tool uses Llama3 via Groq API to extract and standardize resume information. 
Please review the generated resume for accuracy before use.
""")