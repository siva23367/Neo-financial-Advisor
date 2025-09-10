import streamlit as st
import requests
import os
import json

# --- Streamlit Page Config ---
st.set_page_config(page_title="NeoFinancial Advisor", layout="wide")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")

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

# Get LLM provider and model from environment variables
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")

# Load API key based on provider
if LLM_PROVIDER == "groq":
    API_KEY = os.getenv("GROQ_API_KEY")
    if not API_KEY:
        st.error("❌ Groq API key not found. Please set GROQ_API_KEY in your environment.")
        st.stop()
else:
    st.error(f"❌ Unsupported LLM provider: {LLM_PROVIDER}")
    st.stop()

# Keep chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

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
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            
            # Prepare messages for the API
            messages = [{"role": "system", "content": "You are a helpful financial advisor. Provide accurate and helpful advice about investments, markets, and portfolio management."}]
            
            # Add conversation history
            for msg in st.session_state.messages:
                messages.append({"role": msg["role"], "content": msg["content"]})
            
            payload = {
                "model": MODEL_NAME,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1024,
                "top_p": 1,
                "stream": False
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            
            # Check if response is successful
            if response.status_code == 200:
                try:
                    result = response.json()
                    answer = result["choices"][0]["message"]["content"]
                except (json.JSONDecodeError, KeyError) as e:
                    answer = f"Error parsing API response: {str(e)}. Response: {response.text[:200]}"
            else:
                answer = f"API Error {response.status_code}: {response.text[:200]}"

        except requests.exceptions.Timeout:
            answer = "⚠️ Request timed out. Please try again."
        except Exception as e:
            answer = f"❌ An error occurred: {str(e)}"

    # Store assistant message
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)
