# 📄 Intelligent Document Search

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-100000?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
## 🚀 Live Demo

**👉 [Click here to try the live app!](https://huggingface.co/spaces/Umar519/intelligent-document-search)**
## 📖 Overview

**Intelligent Document Search** is a production-ready **RAG (Retrieval-Augmented Generation)** application that allows users to upload PDF documents and ask natural language questions. The system intelligently extracts relevant information and provides accurate answers using **Groq's Llama 3.1 8B model**.

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 📄 **PDF Upload** | Upload any text-based PDF document |
| 🔍 **RAG Architecture** | Retrieves relevant context before generating answers |
| 💬 **Natural Language Q&A** | Ask questions in plain English |
| 🎨 **Beautiful UI** | Colored chat bubbles with dark theme |
| 📊 **Document Stats** | Shows character count and page numbers |
| 💾 **Session Memory** | Maintains chat history during session |
| ⚡ **Fast Responses** | Powered by Groq's ultra-fast inference |
| 🆓 **Free Tier** | 30 requests/minute, 14,400 requests/day |

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web application framework |
| **Groq API** | LLM inference (Llama 3.1 8B) |
| **PyPDF2** | PDF text extraction |
| **RAG Architecture** | Context retrieval & generation |
| **Python** | Backend logic |

## 🏗️ Architecture
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Upload │────▶│ Extract │────▶│ Store │
│ PDF │ │ Text │ │ Context │
└─────────────┘ └─────────────┘ └─────────────┘
│
▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Display │◀────│ Generate │◀────│ Retrieve │
│ Answer │ │ with │ │ Relevant │
│ │ │ Groq AI │ │ Context │
└─────────────┘ └─────────────┘ └─────────────┘

## 📦 Installation

### Prerequisites
- Python 3.9+
- Groq API key (free)


# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

# Run the app
streamlit run app.py
📁 Project Structure
intelligent-document-search/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                   # API key (not in repo)
├── .gitignore            # Git ignore rules
├── README.md             # Documentation
└── src/                  # Source modules (optional)
    ├── ingest.py
    ├── query.py
    └── utils.py
🎯 Usage Guide
Upload a PDF - Click "Browse files" in the sidebar

Process Document - Click "Process Document" button

Ask Questions - Type your question in the chat input

Get Answers - AI responds based on document content

Example Questions
"What is this document about?"

"Summarize the main points"

"What are the key findings?"

"List all important dates mentioned"

"What does page 3 say about [topic]?"

⚡ Performance
Metric	Value
Response Time	2-5 seconds
Context Window	4000 tokens
Free Tier Limits	30 requests/minute
PDF Support	Text-based PDFs
🚀 Deployment
This app is deployed on Streamlit Community Cloud:

Push code to GitHub

Connect repository to share.streamlit.io

Add GROQ_API_KEY in Secrets

Deploy automatically

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

### Setup

```bash
# Clone the repository
git clone https://github.com/Umar5199/intelligent-document-search.git
cd intelligent-document-search


