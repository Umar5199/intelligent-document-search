import os
import streamlit as st
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    text = ""
    try:
        reader = PdfReader(file_path)
        total_pages = len(reader.pages)
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += f"\n--- Page {i+1} of {total_pages} ---\n"
                text += page_text
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def process_document(file_path, file_name):
    """Process and store document"""
    try:
        text = extract_text_from_pdf(file_path)
        
        if not text or len(text.strip()) < 50:
            st.error("Could not extract enough text from PDF. Make sure it's not scanned/images.")
            return None
        
        # Store in session state
        st.session_state.doc_text = text
        st.session_state.current_file = file_name
        st.session_state.messages = []
        
        return True
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def get_document_stats(text):
    """Get document statistics"""
    return {
        "characters": len(text),
        "words": len(text.split()),
        "pages": text.count("--- Page")
    }