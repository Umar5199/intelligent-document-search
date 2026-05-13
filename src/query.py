import streamlit as st
from groq import Groq
import os

class RAGQueryEngine:
    """Query engine using Groq's Llama model"""
    
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"
    
    def ask(self, question, context):
        """Ask a question about the document"""
        try:
            prompt = f"""You are a helpful assistant. Answer the question based ONLY on the provided document text.

DOCUMENT TEXT:
{context[:4000]}

QUESTION: {question}

INSTRUCTIONS:
1. Answer based ONLY on the text above
2. If the answer isn't in the text, say "I cannot find this in the document"
3. Be concise and accurate
4. Include page numbers if mentioned

ANSWER:"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful document Q&A assistant. Answer based only on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def test_connection(self):
        """Test if API is working"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            return True
        except:
            return False