import hashlib
import os

def get_file_hash(file_path: str) -> str:
    """Generate hash of file for caching"""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()

def get_file_icon(filename: str) -> str:
    """Return emoji icon based on file type"""
    ext = filename.split('.')[-1].lower()
    icons = {
        'pdf': '📕',
        'txt': '📄',
        'docx': '📘',
        'md': '📝'
    }
    return icons.get(ext, '📎')

def format_answer(answer: str) -> str:
    """Format the answer for better display"""
    return answer.strip()

def get_document_summary(text: str, max_length: int = 200) -> str:
    """Get a summary of the document"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list:
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if len(chunk.strip()) > 50:
            chunks.append(chunk)
        start = end - overlap
    return chunks