'''

import streamlit as st
from models.llm import ChatModel
from models.embeddings import EmbeddingModel
from utils.rag_utils import process_documents, retrieve_relevant_chunks
from utils.web_search import web_search
import os
from config.config import load_config

# Load configuration
config = load_config()

# Initialize models
@st.cache_resource
def load_models():
    llm = ChatModel(provider=config['llm_provider'], model_name=config['model_name'])
    embedding_model = EmbeddingModel()
    return llm, embedding_model

# Main application
def main():
    st.title("💰 NeoFinancial Advisor")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "response_mode" not in st.session_state:
        st.session_state.response_mode = "concise"
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        # Response mode toggle
        response_mode = st.radio(
            "Response Mode:",
            ["Concise", "Detailed"],
            index=0 if st.session_state.response_mode == "concise" else 1
        )
        st.session_state.response_mode = response_mode.lower()
        
        # Document upload for RAG
        uploaded_files = st.file_uploader(
            "Upload financial documents",
            type=["pdf", "txt", "docx"],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            with st.spinner("Processing documents..."):
                process_documents(uploaded_files, embedding_model)
    
    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User input
    if prompt := st.chat_input("Ask about investments, markets, or portfolio advice"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Retrieve relevant information from documents
                relevant_info = retrieve_relevant_chunks(prompt, embedding_model)
                
                # If no relevant info found, perform web search
                if not relevant_info:
                    relevant_info = web_search(prompt)
                
                # Generate response based on mode
                response = llm.generate_response(
                    prompt=prompt,
                    context=relevant_info,
                    response_mode=st.session_state.response_mode
                )
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    llm, embedding_model = load_models()
    main()
'''

import streamlit as st
from models.llm import ChatModel
from models.embeddings import EmbeddingModel
from utils.rag_utils import process_documents, retrieve_relevant_chunks
from utils.web_search import web_search
import os
from config.config import load_config

# Load configuration
config = load_config()

# Initialize models
@st.cache_resource
def load_models():
    llm = ChatModel(provider=config['llm_provider'], model_name=config['model_name'])
    embedding_model = EmbeddingModel()
    return llm, embedding_model

# Main application
def main():
    st.title("💰 NeoFinancial Advisor")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "response_mode" not in st.session_state:
        st.session_state.response_mode = "concise"
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        # Response mode toggle
        response_mode = st.radio(
            "Response Mode:",
            ["Concise", "Detailed"],
            index=0 if st.session_state.response_mode == "concise" else 1
        )
        st.session_state.response_mode = response_mode.lower()
        
        # Document upload for RAG
        uploaded_files = st.file_uploader(
            "Upload financial documents",
            type=["pdf", "txt", "docx"],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            try:
                with st.spinner("Processing documents..."):
                    process_documents(uploaded_files, embedding_model)
            except Exception as e:
                st.error(f"❌ Error processing documents: {str(e)}")
    
    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User input
    if prompt := st.chat_input("Ask about investments, markets, or portfolio advice"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Retrieve relevant information from documents
                    relevant_info = retrieve_relevant_chunks(
                        prompt,
                        embedding_model
                    )
                    
                    # If no relevant info found, perform web search
                    if not relevant_info:
                        relevant_info = web_search(prompt)
                    
                    # Generate response based on mode
                    response = llm.generate_response(
                        prompt=prompt,
                        context=relevant_info,
                        response_mode=st.session_state.response_mode
                    )
                    
                except Exception as e:
                    response = f"❌ Error generating response: {str(e)}"
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    try:
        llm, embedding_model = load_models()
        main()
    except Exception as e:
        st.error(f"❌ Critical error starting app: {str(e)}")
