from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title="Générateur d'Histoires avec Ollama")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Bienvenue sur le générateur d'histoires courtes avec Ollama"}