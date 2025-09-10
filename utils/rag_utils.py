# utils/rag_utils.py
import os
import PyPDF2
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

def process_documents(uploaded_files, embedding_model):
    """Process uploaded documents and add them to the embedding model"""
    for uploaded_file in uploaded_files:
        text = extract_text_from_file(uploaded_file)
        if text:
            # Split text into chunks (you can adjust chunk size)
            chunks = split_text_into_chunks(text, chunk_size=500)
            embedding_model.add_document(text, chunks)

def extract_text_from_file(uploaded_file):
    """Extract text from different file formats"""
    try:
        if uploaded_file.type == "application/pdf":
            return extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "text/plain":
            return uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return extract_text_from_docx(uploaded_file)
        else:
            print(f"Unsupported file type: {uploaded_file.type}")
            return None
    except Exception as e:
        print(f"Error extracting text from {uploaded_file.name}: {e}")
        return None

def extract_text_from_pdf(uploaded_file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def extract_text_from_docx(uploaded_file):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(uploaded_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return None

def split_text_into_chunks(text, chunk_size=500):
    """Split text into chunks of approximately chunk_size characters"""
    chunks = []
    words = text.split()
    current_chunk = []
    current_size = 0
    
    for word in words:
        if current_size + len(word) + 1 > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_size = 0
        
        current_chunk.append(word)
        current_size += len(word) + 1  # +1 for space
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def retrieve_relevant_chunks(query, embedding_model):
    """Retrieve relevant document chunks using the embedding model"""
    try:
        # Use the embedding model's find_similar method
        relevant_chunks = embedding_model.find_similar(query)
        return relevant_chunks
    except Exception as e:
        print(f"Error retrieving relevant chunks: {e}")
        return []