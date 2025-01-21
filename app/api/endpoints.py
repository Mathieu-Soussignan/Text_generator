from fastapi import APIRouter
from app.services.story_generator import generate_story
from app.schemas.story import StoryRequest, StoryResponse

router = APIRouter()

@router.post("/generate/", response_model=StoryResponse)
def generate(request: StoryRequest):
    # Appeler la fonction avec les nouveaux paramètres
    story = generate_story(request.prompt, request.max_length, request.genre)
    return {"prompt": request.prompt, "story": story}