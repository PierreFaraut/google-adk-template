import os
import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
from dotenv import load_dotenv

load_dotenv()

# Configuration
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_DB_URL = "sqlite:///./habit```ta.db"
ALLOWED_ORIGINS = ["*"]  # À restreindre en production

# ✨ Magie ADK : Création automatique de l'app FastAPI
app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,           # Répertoire contenant vos agents
    session_service_uri=SESSION_DB_URL,  # Votre DB de sessions
    allow_origins=ALLOWED_ORIGINS,
    web=True,                       # Active l'interface Web ADK
)

# Personnalisation de l'API
app.title = "Habit Tracker API"
app.description = "API de suivi d'habitudes avec ADK"
# Ajout d'endpoints personnalisés
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/agent-info")
async def agent_info():
    from habit_tracker import agent
    return {
        "agent_name": agent.root_agent.name,
        "tools": [t.__name__ for t in agent.root_agent.tools]
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
