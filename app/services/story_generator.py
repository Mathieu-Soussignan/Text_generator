import subprocess
from app.core.config import settings

def generate_story(prompt: str, max_length: int = 300) -> str:
    """
    Génère une histoire en français à partir d'un prompt en utilisant la CLI Ollama.
    """
    try:
        # Directive avancée pour l'IA
        adjusted_prompt = (
            f"Important : écris uniquement en français, sans utiliser d'autres langues. Toute réponse partiellement en anglais est interdite. "
            f"Tu es un expert en narration et en création d'histoires captivantes. "
            f"Écris une histoire immersive et cohérente en français uniquement. "
            f"Utilise des éléments classiques de narration : une introduction intrigante, un développement immersif "
            f"et une conclusion mémorable. Assure-toi que l'histoire contient au moins {max_length} mots. "
            f"Voici le début de l'histoire : {prompt}"
        )


        result = subprocess.run(
            ["ollama", "run", settings.OLLAMA_MODEL],
            input=adjusted_prompt,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            raise Exception(f"Erreur Ollama CLI : {result.stderr.strip()}")
    except Exception as e:
        raise Exception(f"Erreur lors de la génération de l'histoire : {e}")