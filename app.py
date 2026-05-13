import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader
import os

# Manual function to read .env file (bypasses dotenv package)
def read_env_file():
    """Read .env file manually"""
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value
                        return value
    except FileNotFoundError:
        return None

# Get API key manually
GROQ_API_KEY = read_env_file()

if not GROQ_API_KEY:
    st.error("❌ Could not read GROQ_API_KEY from .env file!")
    st.info("Make sure .env file exists with: GROQ_API_KEY=your_key_here")
    st.stop()

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Document Q&A Bot", page_icon="📄", layout="wide")

# Custom CSS for colored chat messages
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}

.main-header {
    text-align: center;
    color: white;
    padding: 1.5rem;
    border-radius: 10px;
    background: linear-gradient(90deg, #4285f4, #ea4335, #fbbc04, #34a853);
    margin-bottom: 2rem;
}

.main-header h1 {
    margin: 0;
    font-size: 2.5rem;
}

.main-header p {
    margin: 0.5rem 0 0;
    opacity: 0.9;
}

.stButton > button {
    background: linear-gradient(90deg, #4285f4, #ea4335);
    color: white;
    border: none;
    border-radius: 20px;
    padding: 0.5rem 1.5rem;
    font-weight: bold;
}

.stButton > button:hover {
    transform: scale(1.02);
    transition: 0.2s;
}

/* Chat message styling */
.chat-message {
    padding: 15px;
    border-radius: 15px;
    margin: 10px 0;
    animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.user-message {
    background: linear-gradient(135deg, #4285f4, #5a9ef5);
    color: white;
    border-left: 4px solid #fff;
}

.bot-message {
    background: linear-gradient(135deg, #34a853, #4cbb6b);
    color: white;
    border-left: 4px solid #fff;
}

.user-message strong, .bot-message strong {
    font-size: 1rem;
    display: block;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📄 Document Q&A Bot</h1>
    <p>Powered by Groq AI • Llama 3.1 • RAG Architecture • Free Tier</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'doc_text' not in st.session_state:
    st.session_state.doc_text = ""
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_file' not in st.session_state:
    st.session_state.current_file = None

def ask_question(question, context):
    """Ask question using Groq's Llama model"""
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

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
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

# Sidebar
with st.sidebar:
    st.subheader("📁 Upload PDF Document")
    
    # Show API status
    try:
        test_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        st.success("✅ Groq API Connected")
        st.caption("Model: Llama 3.1 8B Instant")
    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")
    
    st.divider()
    
    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'], help="Upload a PDF document to ask questions about")
    
    if uploaded_file:
        st.info(f"📕 **File:** {uploaded_file.name}\n📏 **Size:** {uploaded_file.size/1024:.1f} KB")
        
        if st.button("📖 Process Document", type="primary", use_container_width=True):
            with st.spinner("Reading and processing PDF..."):
                from PyPDF2 import PdfReader
                reader = PdfReader(uploaded_file)
                text = ""
                for i, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Page {i+1} of {len(reader.pages)} ---\n"
                        text += page_text
                
                if text and len(text.strip()) > 100:
                    st.session_state.doc_text = text
                    st.session_state.current_file = uploaded_file.name
                    st.session_state.messages = []
                    st.success(f"✅ Successfully loaded {uploaded_file.name}")
                    st.info(f"📊 **Stats:** {len(text)} characters, {len(reader.pages)} pages")
                    st.balloons()
                else:
                    st.error("Could not extract text from PDF. Make sure it's not a scanned image.")
    
    if st.session_state.current_file:
        st.divider()
        st.success(f"📄 **Active Document:**\n{st.session_state.current_file}")
        
        if st.button("🗑️ Clear Document", use_container_width=True):
            st.session_state.doc_text = ""
            st.session_state.current_file = None
            st.session_state.messages = []
            st.rerun()
    
    st.divider()
    
    # Tips section
    with st.expander("💡 Tips for best results"):
        st.markdown("""
        - **Use PDFs with selectable text** (not scanned images)
        - **Ask specific questions** for better answers
        - **The bot only answers** from your uploaded document
        - **Maximum 4000 characters** per question context
        - **Free tier limits:** 30 requests per minute
        """)
    
    with st.expander("ℹ️ How it works"):
        st.markdown("""
        1. **Upload** a PDF document
        2. **Process** - Extracts text from PDF
        3. **Ask** questions in natural language
        4. **Get** accurate answers based on your document only
        
        **Tech Stack:**
        - Groq API (Llama 3.1 8B)
        - RAG Architecture
        - Streamlit UI
        - PyPDF2 for text extraction
        """)

# Main chat area
st.subheader("💬 Ask Questions About Your Document")

if not st.session_state.doc_text:
    st.info("👈 **Please upload a PDF document from the sidebar to get started**")
    
    # Show example
    with st.expander("📖 Example Questions to Ask"):
        st.markdown("""
        Once you upload a document, you can ask questions like:
        - *"What is this document about?"*
        - *"Summarize the main points"*
        - *"What are the key findings?"*
        - *"List all important dates mentioned"*
        - *"What does page 3 say about [topic]?"*
        """)
else:
    st.success(f"📄 **Active Document:** {st.session_state.current_file}")
    
    # Display chat history with colored bubbles
    for msg in st.session_state.messages:
        # User message - Blue bubble
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>🧑 You</strong><br>
            {msg['question']}
        </div>
        """, unsafe_allow_html=True)
        
        # Assistant message - Green bubble
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>🤖 AI Assistant</strong><br>
            {msg['answer']}
        </div>
        """, unsafe_allow_html=True)
    
    # Question input
    question = st.chat_input("Ask a question about your document...")
    
    if question:
        # Generate response
        with st.spinner("🤖 Analyzing document with Groq AI..."):
            context = st.session_state.doc_text[:4000]
            answer = ask_question(question, context)
            
            # Save to history
            st.session_state.messages.append({"question": question, "answer": answer})
            st.rerun()
    
    # Clear chat button
    if st.session_state.messages:
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("🗑️ Clear Chat"):
                st.session_state.messages = []
                st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #888; font-size: 0.8rem;'>Built with ❤️ • Groq API (Llama 3.1 8B) • Streamlit • RAG Architecture • Free Tier</p>",
    unsafe_allow_html=True
)