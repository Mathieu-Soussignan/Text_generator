from app.services.story_generator import generate_story

def test_generate_story():
    prompt = "Un magicien découvre un secret."
    story = generate_story(prompt)
    assert isinstance(story, str)
    assert len(story) > 0