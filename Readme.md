# Ollama Interface

A full-stack chat application that allows you to interact with AI models hosted through Ollama. This project features a React frontend and FastAPI backend with SQLite database for chat history persistence.

## Features

- 🤖 Integration with Ollama AI models
- 💬 MultiSession chat interface
- 📝 Persistent chat history
- 🖥️ CodeBlock syntax highlighting
- 🔄 SessionManagement capabilities


## Installation

### prerequisites

- Node.js (v16+)
- Python (v3.8+)
- Ollama installed and running

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create .env file in backend directory. And put contents
```bash
    DB_PATH = "data/assistant.db"
```

### Frontend Setup
```bash
cd frontend
npm install
```

## Starting pplication
```bash
# In one terminal
cd backend
python3 app.py
# In another terminal
cd frontend
npm run dev
```

## Key notes
- Tested sucessfully with deepseek-r1 (shows it's thoughts)
- Tested Phi-4 mini