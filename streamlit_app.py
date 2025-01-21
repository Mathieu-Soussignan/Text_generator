# Importations
import streamlit as st
import requests
from fpdf import FPDF  # Importer FPDF pour générer des PDF

# Configuration
API_URL = "http://127.0.0.1:8000/generate/"
# Si vous utilisez ngrok, décommentez la ligne suivante et remplacez l'URL
# API_URL = "https://c837-185-61-190-198.ngrok-free.app/generate"

# Titre et description
st.title("Bienvenue sur Story Maker !")
st.write("Cette application vous permet de générer des histoires fantastiques en utilisant l'IA.")
st.write("Entrez un prompt en français et laissez l'IA générer une histoire rien que pour vous.")

# Initialisation de l'état de session pour la gestion des prompts
if "prompt" not in st.session_state:
    st.session_state.prompt = "Il était une fois un chevalier courageux..."

# Sidebar - Paramètres
st.sidebar.title("Paramètres de génération")

# Paramètres ajustables par l'utilisateur
max_length = st.sidebar.slider("Longueur de l'histoire (en mots) :", 100, 400, 200)
genre = st.sidebar.selectbox(
    "Genre de l'histoire :",
    ["Aventure", "Fantastique", "Comédie", "Horreur", "Science-fiction"]
)

# Exemples de prompts prédéfinis
examples = [
    "Il était une fois un magicien qui voulait apprendre un sort interdit...",
    "Dans une galaxie lointaine, un pilote de vaisseau spatial découvre un signal étrange...",
    "Un détective enquête sur une série de disparitions mystérieuses dans une petite ville...",
    "Un chevalier intrépide reçoit une mission impossible : récupérer une relique perdue dans un royaume maudit...",
    "Une jeune fille découvre qu'elle peut communiquer avec les animaux et part en quête de sauver une forêt enchantée...",
    "Un scientifique brillant mais controversé invente une machine capable de remonter dans le temps...",
    "Un groupe d'amis se perd dans une montagne où d'étranges phénomènes se produisent chaque nuit...",
    "Un écrivain en panne d'inspiration trouve un mystérieux carnet qui donne vie à tout ce qu'il écrit...",
    "Dans une ville plongée dans l'obscurité, un héros masqué se bat pour rétablir la lumière et la justice...",
    "Un enfant curieux trouve une clé dorée qui ouvre la porte vers un monde parallèle plein de secrets...",
    "Un pirate légendaire part à la recherche d'un trésor oublié, gardé par des créatures mythiques..."
]

# Sélection d'un exemple prédéfini
selected_example = st.sidebar.selectbox("Choisissez un exemple :", examples)

# Bouton pour utiliser un exemple
if st.sidebar.button("Utiliser cet exemple"):
    st.session_state.prompt = selected_example

# Champ principal pour le prompt
prompt = st.text_area("Votre prompt :", st.session_state.prompt)

# Mise à jour de l'état du prompt après modification
st.session_state.prompt = prompt

# Fonction pour générer un fichier PDF avec mise en forme
def generate_pdf(story: str, title: str = "Votre Histoire Générée") -> bytes:
    """
    Génère un fichier PDF à partir de l'histoire générée avec une mise en forme esthétique.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Titre
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(10)

    # Contenu de l'histoire
    pdf.set_font("Arial", size=12)
    for line in story.split('\n'):
        pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'))

    # Sauvegarder le PDF en mémoire
    return pdf.output(dest='S').encode('latin-1')

# Bouton de génération
if st.button("Générer l'histoire"):
    if not prompt.strip():
        st.error("Veuillez entrer un prompt avant de générer une histoire.")
    else:
        # Affichage d'un spinner pendant la génération
        with st.spinner("Génération en cours..."):
            try:
                # Requête POST à l'API FastAPI
                enriched_prompt = (
                    f"Tu es un expert en narration et en écriture d'histoires captivantes. "
                    f"Écris une histoire immersive et uniquement en français. "
                    f"Voici le début de l'histoire : {prompt}"
                )
                response = requests.post(API_URL, json={
                    "prompt": enriched_prompt,
                    "max_length": max_length,
                    "genre": genre
                })

                if response.status_code == 200:
                    # Récupération et affichage de l'histoire générée
                    story = response.json().get("story", "Aucune histoire générée.")
                    st.success("Voici votre histoire :")
                    st.write(story)

                    # Bouton de téléchargement pour l'histoire au format TXT
                    st.download_button(
                        label="Télécharger l'histoire en TXT",
                        data=story,
                        file_name="histoire.txt",
                        mime="text/plain"
                    )

                    # Bouton de téléchargement pour l'histoire au format PDF
                    pdf_data = generate_pdf(story, title="Histoire générée par StoryMaker")
                    st.download_button(
                        label="Télécharger l'histoire en PDF",
                        data=pdf_data,
                        file_name="histoire.pdf",
                        mime="application/pdf"
                    )
                else:
                    # Gestion des erreurs renvoyées par l'API
                    error_message = response.json().get("detail", "Erreur inconnue.")
                    st.error(f"Erreur de l'API ({response.status_code}): {error_message}")
            except Exception as e:
                # Gestion des erreurs de connexion
                st.error(f"Erreur de connexion à l'API : {e}")