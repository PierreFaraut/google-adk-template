from dotenv import load_dotenv

load_dotenv()

import os
import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
import agentops

AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
agentops.init(api_key=AGENTOPS_API_KEY, default_tags=["google adk"])


# Configuration
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))

if os.environ.get("ENV_MODE", 'dev').lower() == "prod":
    SESSION_DB_URL = os.environ.get("SESSION_DB_URL")
else:
    ## sqlite db for local development
    SESSION_DB_URL = os.environ.get("sqlite:///./sessions.db")
ALLOWED_ORIGINS = ["*"] 

app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,       
    session_service_uri=SESSION_DB_URL, 
    allow_origins=ALLOWED_ORIGINS,
    web=True,                    
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
