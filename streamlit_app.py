# Importations
import streamlit as st
import requests

# Configuration
# API_URL = "http://127.0.0.1:8000/generate/"
API_URL = "https://0fb4-185-61-190-198.ngrok-free.app/generate"

# Titre et description
st.title("Bienvenue sur StoryMaker !")
st.write("Cette application vous permet de générer des histoires captivantes en utilisant l'IA.")
st.write("Entrez un prompt en français et laissez l'IA générer une histoire captivante.")

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
    "Un détective enquête sur une série de disparitions mystérieuses dans une petite ville..."
]

selected_example = st.sidebar.selectbox("Choisissez un exemple :", examples)

# Bouton pour utiliser un exemple
if st.sidebar.button("Utiliser cet exemple"):
    st.session_state.prompt = selected_example

# Champ principal pour le prompt
prompt = st.text_area("Votre prompt :", st.session_state.prompt)

# Bouton de génération
if st.button("Générer l'histoire"):
    if not prompt.strip():
        st.error("Veuillez entrer un prompt avant de générer une histoire.")
    else:
        # Affichage d'un spinner pendant la génération
        with st.spinner("Génération en cours..."):
            try:
                # Requête POST à l'API FastAPI
                response = requests.post(API_URL, json={
                    "prompt": prompt,
                    "max_length": max_length,
                    "genre": genre
                })

                if response.status_code == 200:
                    # Récupération et affichage de l'histoire générée
                    story = response.json().get("story", "Aucune histoire générée.")
                    st.success("Voici votre histoire :")
                    st.write(story)

                    # Bouton de téléchargement pour l'histoire
                    st.download_button(
                        label="Télécharger l'histoire",
                        data=story,
                        file_name="histoire.txt",
                        mime="text/plain"
                    )
                else:
                    # Gestion des erreurs renvoyées par l'API
                    error_message = response.json().get("detail", "Erreur inconnue.")
                    st.error(f"Erreur de l'API ({response.status_code}): {error_message}")
            except Exception as e:
                # Gestion des erreurs de connexion
                st.error(f"Erreur de connexion à l'API : {e}")