# 📞 Customer Support Voice Agent (RAG + TTS)

An end-to-end voice-enabled customer support assistant built with:

- **LangChain** for retrieval-augmented generation (RAG)
- **OpenAI** for embeddings + generative responses
- **ChromaDB** for vector storage
- **Gradio** for a clean, interactive UI
- **Custom web scraper** (requests + BeautifulSoup) for ingesting documentation

This project allows users to ask natural-language questions about uploaded or scraped docs, and get answers read aloud using OpenAI’s text-to-speech engine.

---

## 🚀 Features

### **1. Knowledge Base Building (RAG)**
- Scrapes documentation pages using a custom `requests + BeautifulSoup` function  
- Cleans HTML → extracts readable text  
- Splits docs into semantic chunks (LangChain text splitters)  
- Generates embeddings using `OpenAIEmbeddings`  
- Stores vectors in **ChromaDB**  
- Fully persistent between runs

### **2. Voice AI Agent**
- Answers queries using a LangChain retrieval chain  
- Supports multiple OpenAI TTS voices:
  `alloy`, `ash`, `ballad`, `coral`, `echo`, `fable`, `onyx`, `nova`, `sage`, `shimmer`, `verse`
- Streams back natural-sounding MP3 audio  
- Provides a download link for audio responses

### **3. Gradio Interface**
- Clean chat-style question box  
- Audio output widget  
- Real-time document search  
- RAG debug output included (optional)  

---

## 📦 Project Structure

├── app.py # Gradio UI and main agent
├── ingest.py # Build knowledge base (scrape > chunk > embed > save)
├── rag_chain.py # Retrieval + LLM chain definition
├── tts_agent.py # Text-to-speech helper
├── fetch_utils.py # (Optional) Your custom website extractor
│
├── chroma_db/ # Auto-created: vector store persistence
├── docs/ # (Optional) local markdown/text docs
│
├── requirements.txt
└── README.md