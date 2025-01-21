from fastapi import APIRouter
from app.schemas.story import StoryRequest, StoryResponse
from app.services.story_generator import generate_story

router = APIRouter()

@router.post("/generate/", response_model=StoryResponse)
def generate(request: StoryRequest):
    story = generate_story(request.prompt)
    return {"prompt": request.prompt, "story": story}