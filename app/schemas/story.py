from pydantic import BaseModel

class StoryRequest(BaseModel):
    prompt: str

class StoryResponse(BaseModel):
    prompt: str
    story: str