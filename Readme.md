# aiAssistant

A full-stack chat application that allows you to interact with AI models hosted through Ollama. This project features a React frontend and FastAPI backend with SQLite database for chat history persistence.

## features

- 🤖 Integration with Ollama AI models
- 💬 MultiSession chat interface
- 📝 Persistent chat history
- 🖥️ CodeBlock syntax highlighting
- 🔄 SessionManagement capabilities


## installation

### prerequisites

- Node.js (v16+)
- Python (v3.8+)
- Ollama installed and running

### backendSetup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

### frontendSetup
cd frontend
npm install


# In one terminal
cd backend
python3 app.py
# In another terminal
cd frontend
npm run dev