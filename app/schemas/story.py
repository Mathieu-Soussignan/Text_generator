from pydantic import BaseModel

# Modèle pour les requêtes
class StoryRequest(BaseModel):
    prompt: str
    max_length: int = 200  # Longueur par défaut
    genre: str = "Aventure"  # Genre par défaut

# Modèle pour les réponses
class StoryResponse(BaseModel):
    prompt: str
    story: str