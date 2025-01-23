# Importations
import streamlit as st
import requests
from fpdf import FPDF  # Importer FPDF pour générer des PDF
from PIL import Image, ImageDraw # Pour générer un fichier PDF avec mise en forme et logo
from collections import Counter
import matplotlib.pyplot as plt
from io import BytesIO

# Configuration
API_URL = "http://127.0.0.1:8000/generate/"
# Si vous utilisez ngrok, décommentez la ligne suivante et remplacez l'URL
# API_URL = "https://c837-185-61-190-198.ngrok-free.app/generate"

# Fonction pour appliquer les thèmes
def apply_theme(theme: str):
    """
    Applique un thème visuel en injectant du CSS en utilisant les classes spécifiques identifiées dans l'application.
    """
    if theme == "Clair":
        st.markdown(
            """
            <style>
            body {
                background-color: #FFFFFF;
                color: #000000;
            }
            .stSidebar {
                background-color: #F0F2F6;
            }
            .stButton > button {
                background-color: #007BFF;
                color: #FFFFFF;
                border-radius: 5px;
            }
            .stButton > button:hover .st {
                background-color: #005A9E;
            }
            /* Styles pour les titres */
            .st-emotion-cache-1espb9k h1, .st-emotion-cache-1espb9k h2, .st-emotion-cache-1espb9k h3 {
                color: #333333;
                font-weight: bold;
            }
            /* Styles pour les paragraphes */
            .st-emotion-cache-14553y9 p, .st-emotion-cache-1cvow4s p, st-emotion-cache-1qrd9al e121c1cl0 p, .st-emotion-cache-1qrd9al p, .st-emotion-cache-1vsah7k p {
                color: #555555;
            }
            /* Exclure le texte du bouton */
            button .st-emotion-cache-1vsah7k p {
                color: #FFFFFF !important;
            }
            textarea, select {
                background-color: #FFFFFF;
                color: #000000;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    elif theme == "Sombre":
        st.markdown(
            """
            <style>
            body {
                background-color: #121212;
                color: #FFFFFF;
            }
            .stSidebar {
                background-color: #333333;
            }
            .stButton > button {
                background-color: #007BFF;
                color: #FFFFFF;
                border-radius: 5px;
            }
            /* Styles pour les titres */
            .st-emotion-cache-1espb9k h1, .st-emotion-cache-1espb9k h2, .st-emotion-cache-1espb9k h3 {
                color: #FFFFFF;
                font-weight: bold;
            }
            /* Styles pour les paragraphes */
            .st-emotion-cache-14553y9 p {
                color: #CCCCCC;
            }
            textarea, select {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    elif theme == "Vintage":
        st.markdown(
            """
            <style>
            body {
                background-color: #FAEBD7;
                color: #5A4632;
                font-family: 'Courier New', Courier, monospace;
            }
            .stSidebar {
                background-color: #FFE4C4;
            }
            .stButton > button {
                background-color: #8B4513;
                color: #FFFFFF;
                border-radius: 5px;
            }
            /* Styles pour les titres */
            .st-emotion-cache-1espb9k h1, .st-emotion-cache-1espb9k h2, .st-emotion-cache-1espb9k h3 {
                color: #8B4513;
                font-weight: bold;
            }
            /* Styles pour les paragraphes */
            .st-emotion-cache-14553y9 p, .st-emotion-cache-1qrd9al p, .st-emotion-cache-1vsah7k p {
                color: #5A4632;
            }
            /* Exclure le texte du bouton */
            button .st-emotion-cache-1vsah7k p {
                color: #FFFFFF !important;
            }
            textarea, select {
                background-color: #FFF8DC;
                color: #5A4632;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

# Titre et description
st.title("Bienvenue sur Story Maker !")
st.write("Cette application vous permet de générer des histoires fantastiques en utilisant l'IA.")
st.write("Entrez un prompt en français et laissez l'IA générer une histoire rien que pour vous.")

# Initialisation de l'état de session
if "prompt" not in st.session_state:
    st.session_state.prompt = "Il était une fois un chevalier courageux..."

if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar - Paramètres
st.sidebar.title("Paramètres de personnalisation et de génération")

# Sélecteur de thème dans la barre latérale
theme = st.sidebar.selectbox(
    "Choisissez un thème :",
    ["Clair", "Sombre", "Vintage"]
)

# Appliquez le thème sélectionné
apply_theme(theme)

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

# Fonction pour arrondir une image
def round_image(image_path: str, output_path: str = "rounded_logo.png") -> str:
    """
    Transforme une image en forme arrondie et sauvegarde le résultat.
    """
    with Image.open(image_path) as im:
        # Assurez-vous que l'image est carrée
        size = min(im.size)
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        output = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        output.paste(im, (0, 0), mask)
        output.save(output_path, format="PNG")
        return output_path

# Fonction pour générer le PDF
def generate_pdf(story: str, title: str = "Votre Histoire Générée", logo_path: str = "story_maker_logo.png") -> bytes:
    """
    Génère un fichier PDF à partir de l'histoire générée avec une mise en forme esthétique et un logo.
    """
    rounded_logo_path = round_image(logo_path)

    class PDF(FPDF):
        def header(self):
            # Ajouter un logo arrondi uniquement sur la première page
            if self.page_no() == 1:
                try:
                    self.image(rounded_logo_path, x=10, y=8, w=30)  # Positionner le logo arrondi
                except RuntimeError:
                    self.set_font("Arial", "I", 10)
                    self.set_text_color(255, 0, 0)  # Couleur rouge pour signaler l'erreur
                    self.cell(0, 10, "Erreur : Logo introuvable", align="L")
            # Titre de l'en-tête
            self.set_font("Arial", "B", 12)
            self.set_text_color(128, 128, 128)  # Couleur grise
            self.cell(0, 10, "StoryMaker - Générateur d'Histoires", align="C", ln=True)
            self.ln(10)

        def footer(self):
            # Position à 1.5 cm du bas
            self.set_y(-15)
            self.set_font("Arial", "I", 10)
            self.set_text_color(128, 128, 128)
            # Numéro de page
            self.cell(0, 10, f"Page {self.page_no()}", align="C")

    # Créer une instance du PDF
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Titre principal
    pdf.set_font("Arial", style="B", size=16)
    pdf.set_text_color(33, 37, 41)  # Couleur sombre pour le titre
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(10)

    # Introduction ou citation stylisée
    pdf.set_font("Times", "I", 12)
    pdf.set_text_color(100, 100, 100)  # Couleur grise pour l'intro
    pdf.multi_cell(0, 10, "Une histoire unique créée avec soin par l'intelligence artificielle de StoryMaker.")
    pdf.ln(5)

    # Contenu de l'histoire
    pdf.set_font("Times", size=12)
    pdf.set_text_color(50, 50, 50)  # Couleur légèrement sombre pour le texte principal
    for line in story.split('\n'):
        pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'))

    # Ajouter une séparation ou fin d'histoire
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(150, 150, 150)  # Couleur grise pour le texte de fin
    pdf.cell(0, 10, "- Fin de l'histoire -", align="C")

    # Sauvegarder le PDF en mémoire
    return pdf.output(dest='S').encode('latin-1')

# Utilisation dans le Streamlit
from collections import Counter
import matplotlib.pyplot as plt
from io import BytesIO

# Fonction pour calculer les statistiques d'écriture
def calculate_statistics(story: str) -> dict:
    """
    Calcule des statistiques basiques sur l'histoire générée.
    """
    words = story.split()
    num_words = len(words)
    num_characters = len(story)
    
    # Compter la fréquence des mots (mots clés les plus fréquents)
    word_counts = Counter(words)
    most_common_words = word_counts.most_common(5)  # Top 5 mots les plus fréquents

    return {
        "num_words": num_words,
        "num_characters": num_characters,
        "most_common_words": most_common_words,
    }

# Fonction pour tracer la distribution des mots-clés
def plot_word_distribution(word_counts: list) -> BytesIO:
    """
    Génère un graphique de distribution des mots-clés.
    """
    words, counts = zip(*word_counts)
    plt.figure(figsize=(8, 6))
    plt.bar(words, counts, color='skyblue')
    plt.title("Distribution des mots-clés")
    plt.xlabel("Mots")
    plt.ylabel("Fréquence")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Sauvegarder le graphique en mémoire
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)
    plt.close()
    return img_buffer

# Intégration des statistiques dans Streamlit
if st.button("Générer l'histoire"):
    if not prompt.strip():
        st.error("Veuillez entrer un prompt avant de générer une histoire.")
    else:
        with st.spinner("Génération en cours..."):
            try:
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
                    story = response.json().get("story", "Aucune histoire générée.")
                    st.success("Voici votre histoire :")
                    st.write(story)

                    # Calculer les statistiques
                    stats = calculate_statistics(story)
                    st.write("### Statistiques sur l'histoire générée")
                    st.write(f"- **Nombre de mots :** {stats['num_words']}")
                    st.write(f"- **Nombre de caractères :** {stats['num_characters']}")
                    st.write("#### Mots-clés les plus fréquents :")
                    for word, count in stats["most_common_words"]:
                        st.write(f"- {word} : {count} fois")

                    # Afficher un graphique des mots-clés
                    st.write("### Distribution des mots-clés")
                    word_dist_img = plot_word_distribution(stats["most_common_words"])
                    st.image(word_dist_img, caption="Distribution des mots-clés", use_container_width=True)

                    # Ajout de l'histoire et des statistiques à l'historique
                    st.session_state.history.append({"prompt": prompt, "story": story, "stats": stats})

                    # Bouton de téléchargement pour l'histoire au format PDF
                    pdf_data = generate_pdf(story, title="Histoire générée par StoryMaker", logo_path="story_maker_logo.png")
                    st.download_button(
                        label="Télécharger l'histoire en PDF",
                        data=pdf_data,
                        file_name="story_maker.pdf",
                        mime="application/pdf"
                    )
                else:
                    error_message = response.json().get("detail", "Erreur inconnue.")
                    st.error(f"Erreur de l'API ({response.status_code}): {error_message}")
            except Exception as e:
                st.error(f"Erreur de connexion à l'API : {e}")

# Ajout des statistiques dans l'historique
if st.sidebar.checkbox("Afficher l'historique des histoires"):
    st.sidebar.write("## Historique des histoires")
    if st.session_state.history:
        for idx, entry in enumerate(st.session_state.history[::-1], 1):
            with st.sidebar.expander(f"Histoire {idx}"):
                st.write(f"### Prompt :\n{entry['prompt']}")
                st.write(f"### Histoire :\n{entry['story']}")
                
                # Afficher les statistiques enregistrées
                stats = entry.get("stats", {})
                st.write("#### Statistiques :")
                st.write(f"- Nombre de mots : {stats.get('num_words', 'N/A')}")
                st.write(f"- Nombre de caractères : {stats.get('num_characters', 'N/A')}")
                if "most_common_words" in stats:
                    st.write("#### Mots-clés les plus fréquents :")
                    for word, count in stats["most_common_words"]:
                        st.write(f"- {word} : {count} fois")
                
                # Graphique des mots-clés
                if "most_common_words" in stats:
                    word_dist_img = plot_word_distribution(stats["most_common_words"])
                    st.image(word_dist_img, caption="Distribution des mots-clés", use_column_width=True)

                # Ajout d'un bouton pour télécharger directement depuis l'historique
                pdf_data = generate_pdf(entry['story'], title=f"Histoire {idx}", logo_path="story_maker_logo.png")
                st.download_button(
                    label=f"Télécharger Histoire {idx} en PDF",
                    data=pdf_data,
                    file_name=f"histoire_{idx}.pdf",
                    mime="application/pdf",
                    key=f"download_{idx}"
                )
    else:
        st.sidebar.write("Aucune histoire enregistrée pour le moment.")