# **StoryMaker - Générateur d'Histoires avec l'IA**

## **1. Introduction**

**StoryMaker** est une application conçue pour vous permettre de créer facilement des histoires captivantes avec l’aide de l’intelligence artificielle. Grâce à une interface simple développée avec **Streamlit**, vous pouvez personnaliser vos récits en choisissant leur genre, leur longueur et leur contenu. Le backend, construit avec **FastAPI**, communique avec le modèle **Ollama** pour générer des textes de qualité. Que vous soyez amateur de récits ou créateur en quête d’inspiration, StoryMaker vous accompagne dans l’écriture d’histoires uniques.

---

## **2. Définition de la problématique**

### **Problème :**

Dans un monde où les outils d'intelligence artificielle se multiplient, la génération automatisée d'histoires engageantes en langue française reste un défi. Les créateurs de contenu, écrivains et amateurs de récits cherchent des outils :

- Faciles à utiliser.
- Produisant des textes captivants et personnalisables.
- Capables de respecter des contraintes de genre et de style.

### **Objectif :**

Développer une solution intégrée qui permette à l'utilisateur de générer des histoires personnalisées selon ses besoins (longueur, genre) en se basant sur un modèle IA performant, tout en assurant une expérience utilisateur intuitive et fluide.

---

## **3. Fonctionnalités principales**

1. **Personnalisation des histoires** :
   - Choix du genre : Aventure, Fantastique, Comédie, Horreur, Science-fiction.
   - Définition de la longueur de l'histoire (100 à 400 mots).
2. **Exemples prédéfinis** :
   - Plusieurs prompts sont proposés pour inspirer l'utilisateur.
3. **Statistiques d'écriture** :
   - Nombre de mots.
   - Nombre de caractères.
   - Distribution des mots-clés les plus fréquents.
4. **Affichage de l'historique** :
   - Les histoires générées sont sauvegardées et accessibles depuis la barre latérale.
5. **Téléchargement** :
   - Les histoires générées peuvent être téléchargées au format `.txt` ou `.pdf`.
6. **Interface utilisateur intuitive** :
   - Conçue avec **Streamlit**, permettant une navigation simple et rapide.
7. **Backend robuste** :
   - API développée avec **FastAPI** pour gérer les requêtes et communiquer avec le modèle **Ollama**.

---

## **4. Architecture technique**

### **Technologies utilisées** :

- **Frontend** : Streamlit (interface utilisateur).
- **Backend** : FastAPI (gestion des requêtes API).
- **Modèle IA** : Ollama (modèle `llama2` pour la génération de texte).
- **Bibliothèques complémentaires** :
  - **Pillow** pour gérer le logo dans les PDF.
  - **Matplotlib** pour les graphiques.
  - **FPDF** pour la génération de PDF.
- **Serveur local** : Ollama sert les requêtes depuis votre machine ou un serveur dédié.
- **Outils de déploiement** :
  - Local avec **ngrok**.
  - Hébergement cloud possible avec **Render**, **Streamlit Cloud**, ou **AWS**.

### **Diagramme d'architecture** :

```plaintext
Streamlit (frontend)
        |
        v
    FastAPI (backend)
        |
        v
    Ollama (modèle IA)
```

---

## **5. Installation et utilisation**

### **Prérequis** :

- Python 3.8 ou version supérieure.
- Pip pour gérer les dépendances.
- **Ollama** installé sur votre machine locale.
- Optionnel : ngrok pour exposer l'API.

### **Installation** :

1. Clonez le dépôt :
   ```bash
   git clone <lien_du_dépôt>
   cd Texte-Genererator
   ```
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Assurez-vous qu'Ollama est installé et fonctionnel :
   ```bash
   ollama serve
   ```

### **Démarrage de l'application** :

1. Lancez le backend FastAPI :
   ```bash
   uvicorn app.main:app --reload
   ```
2. Lancez l'interface Streamlit :
   ```bash
   streamlit run streamlit_app.py
   ```
3. (Optionnel) Lancez ngrok pour exposer votre API :
   ```bash
   ngrok http 8000
   ```

---

## **6. Utilisation**

1. Accédez à l'application Streamlit dans votre navigateur.
2. **Choisissez** un genre et une longueur pour l'histoire.
3. **Saisissez** ou sélectionnez un prompt depuis la barre latérale.
4. Cliquez sur **"Générer l'histoire"**.
5. Consultez les **statistiques** sur l'histoire générée (nombre de mots, caractères, etc.).
6. **Téléchargement** :
   - Les histoires générées peuvent être téléchargées au format `.pdf`.
7. Consultez l'**historique** des histoires depuis la barre latérale.

---

## **7. Tests**

### **Tests avec Swagger UI** :

Accédez à la documentation interactive générée par FastAPI à :

```
http://127.0.0.1:8000/docs
```

- Envoyez une requête POST à `/generate/` avec un corps JSON :
  ```json
  {
      "prompt": "Il était une fois un chevalier courageux...",
      "max_length": 300,
      "genre": "Fantastique"
  }
  ```

### **Tests depuis Streamlit** :

- Utilisez l'application pour tester les différents paramètres et prompts.

---

## **8. Prochaines améliorations**

1. **Ajout de nouveaux genres ou styles narratifs.**
2. **Hébergement complet sur un serveur cloud.**
3. **Analyse avancée du texte** : Lisibilité, sentiments, etc.
4. **Mode collaboratif** pour écrire à plusieurs.
5. **Génération d'illustrations** pour accompagner les histoires.

---

## **9. Auteurs**

- **Mathieu Soussignan** et **Yamine Aissani**

- Rôles : Développement, conception et implémentation.

- **Contributions clés** :

- Mise en place de l'architecture technique.

- Intégration des modèles d'IA.

- Conception de l'interface utilisateur.

## **10. Licence**

Ce projet est sous licence MIT.