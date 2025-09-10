# 💰 Neo Financial Advisor

An AI-powered financial advisor chatbot built with **Streamlit**, **Groq LLMs**, and **Retrieval-Augmented Generation (RAG)**.  
The app can answer investment, portfolio, and market-related queries with support for **Concise** and **Detailed** response modes.  

---

## 🚀 Features

- **RAG Integration**  
  Upload PDFs, DOCX, or TXT files. The chatbot retrieves relevant chunks using TF-IDF embeddings.  

- **Live Web Search**  
  If document context is missing, the app falls back to real-time web search.  

- **Multiple Response Modes**  
  - *Concise* → short, summarized answers.  
  - *Detailed* → in-depth, structured explanations with examples.  

- **Multi-provider LLM Support**  
  - ✅ Groq (`gemma2-9b-it`)  
  - ✅ Hugging Face fallback (`zephyr-7b-beta`)  
  - ⚠️ OpenAI & Gemini stubs included (will fallback if no billing enabled).  

- **Error Handling**  
  Graceful error messages in case of broken documents, API errors, or missing embeddings.  

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) – UI framework  
- [Groq](https://groq.com/) – LLM provider  
- [Hugging Face Inference API](https://huggingface.co/) – fallback models  
- [scikit-learn](https://scikit-learn.org/) – TF-IDF embeddings  
- [NumPy](https://numpy.org/) – similarity calculations  
- [Requests](https://docs.python-requests.org/) – API calls  
- [python-dotenv](https://pypi.org/project/python-dotenv/) – environment variable handling  

---

## 📂 Project Structure

```
Neo-financial-Advisor/
│
├── app.py                # Main Streamlit app
├── requirements.txt      # Dependencies
│
├── config/
│   └── config.py         # Configuration loader (API keys, defaults)
│
├── models/
│   ├── llm.py            # LLM provider handling (Groq, HF, stubs for OpenAI/Gemini)
│   └── embeddings.py     # TF-IDF embeddings + retrieval
│
├── utils/
│   ├── rag_utils.py      # Document processing + chunking
│   └── web_search.py     # Live web search integration
```

---

## ⚙️ Installation

Clone the repo:

```bash
git clone https://github.com/siva23367/Neo-financial-Advisor.git
cd Neo-financial-Advisor
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate    # Linux/Mac
.venv\Scripts\activate     # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run locally:

```bash
streamlit run app.py
```

---

## 🔑 Environment Variables & Secrets

### Local development
Create a `.env` file in the project root:

```env
LLM_PROVIDER=groq
MODEL_NAME=llama-3.1-8b-instant
GROQ_API_KEY=your_groq_api_key
```

### Streamlit Cloud
In **App Settings → Secrets**, add:

```toml
[groq]
api_key = "your_groq_api_key_here"
```

In `config/config.py`, keys are read from either `os.getenv` or `st.secrets`.

---

## ☁️ Deployment (Streamlit Cloud)

1. Push your repo to GitHub.  
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) → **New App**.  
3. Select:
   - Repo: `siva23367/Neo-financial-Advisor`
   - Branch: `main`
   - Entrypoint: `app.py`  
4. Add API keys in **Secrets Manager**.  
5. Deploy 🎉  

Your app will be live at:
```
https://siva23367-neo-financial-advisor.streamlit.app
```

---

## 📊 Example Questions

- “What is the best way to diversify my portfolio if I only hold tech stocks?”  
- “What are the risks and opportunities of investing in Indian stock markets in 2025?”  
- “I’m 35 with 10 lakhs INR savings. How should I plan for retirement?”  
- “What should I do if the stock market crashes tomorrow?”  

---

## 📑 Deliverables

- ✅ Working chatbot with RAG + Web Search  
- ✅ Concise vs Detailed response modes  
- ✅ Modular project structure  
- ✅ Deployable on Streamlit Cloud  
- ✅ PPT deck (use case, approach, solution, challenges, deployment link)  

---

## 👨‍💻 Author

Developed by **[siva23367](https://github.com/siva23367)**
