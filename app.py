import streamlit as st
import requests
import os
import json
from dotenv import load_dotenv

# Try to load from .env file for local development
load_dotenv()

# --- Streamlit Page Config ---
st.set_page_config(page_title="NeoFinancial Advisor", layout="wide")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Get API key from environment, secrets, or allow manual input
    # Try to get from Streamlit secrets first (for deployment)
    try:
        default_key = st.secrets["GROQ_API_KEY"]
    except (KeyError, FileNotFoundError):
        # Fall back to environment variable (for local development)
        default_key = os.getenv("GROQ_API_KEY", "")
    
    api_key = st.text_input(
        "Groq API Key",
        value=default_key,
        type="password",
        help="Enter your Groq API key from https://console.groq.com"
    )

    response_mode = st.radio(
        "Response Mode:",
        options=["Concise", "Detailed"],
        index=0
    )

    uploaded_files = st.file_uploader(
        "Upload financial documents",
        type=["pdf", "csv", "txt", "docx", "jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) uploaded")

# --- Main App UI ---
st.title("💰 NeoFinancial Advisor")

# Check if API key is available
if not api_key:
    st.error("❌ Please enter your Groq API key in the sidebar to continue.")
    st.stop()

# Keep chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "Hello! I'm your NeoFinancial Advisor. How can I help with your investments, markets, or portfolio questions today?"
    }]

# --- Display chat history ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- User Input ---
if prompt := st.chat_input("Ask about investments, markets, or portfolio advice"):
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Call Groq API with loading spinner
    with st.spinner("🤖 Thinking..."):
        try:
            # Groq API endpoint
            API_URL = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Prepare messages for the API - include system message and conversation history
            messages = [
                {
                    "role": "system", 
                    "content": """You are NeoFinancial Advisor, a helpful AI financial expert. 
                    Provide accurate, helpful advice about investments, markets, and portfolio management.
                    Be clear and concise in your responses."""
                }
            ]
            
            # Add conversation history (recent messages to maintain context)
            for msg in st.session_state.messages[-6:]:  # Keep last 6 messages for context
                messages.append({"role": msg["role"], "content": msg["content"]})
            
            payload = {
                "model": "llama-3.1-8b-instant",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1024,
                "top_p": 1,
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            
            # Check if response is successful
            if response.status_code == 200:
                result = response.json()
                answer = result["choices"][0]["message"]["content"]
            else:
                st.error(f"API Error {response.status_code}")
                answer = f"I'm having trouble connecting to the financial analysis system. Error: {response.status_code}"
                if response.status_code == 401:
                    answer += " - Please check your API key is correct."

        except requests.exceptions.Timeout:
            answer = "⚠️ Request timed out. The financial markets are busy right now. Please try again."
        except requests.exceptions.ConnectionError:
            answer = "⚠️ Connection error. Please check your internet connection and try again."
        except Exception as e:
            answer = f"❌ An unexpected error occurred: {str(e)}"

    # Store assistant message
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)

# Add a footer with info
st.sidebar.markdown("---")
st.sidebar.info(
    """
    **Note:** This financial advisor is powered by AI and should not be considered 
    as professional financial advice. Always consult with a qualified financial 
    advisor before making investment decisions.
    """
)
