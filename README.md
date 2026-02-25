# 🎬 Studio-Brain : Assistant IA pour Pipelines de Production

**Studio-Brain** est un assistant intelligent basé sur l'architecture **RAG (Retrieval-Augmented Generation)**. Il permet aux artistes et techniciens d'interroger la documentation technique (Blender, Unreal Engine, pipelines internes) en langage naturel, tout en garantissant une confidentialité totale via une exécution 100% locale.

---

## 🚀 Fonctionnalités
- **Recherche Sémantique :** Interroge vos PDF techniques sans recherche manuelle.
- **Exécution Locale :** Utilise Ollama et Mistral pour protéger vos données de production.
- **Base de Données Persistante :** L'indexation est stockée sur disque pour un démarrage instantané.
- **Interface Studio :** Interface épurée développée avec Streamlit.

## 🛠️ Installation & Lancement

### 1. Prérequis
- Python 3.10+
- Ollama installé et lancé.
- Modèles à télécharger :
  - ollama pull mistral
  - ollama pull nomic-embed-text

### 2. Configuration du projet
Clonez le dépôt et installez les dépendances :
- git clone https://github.com/lucasdelbecque/studio-rag-ia.git
- cd studio-rag-ia
- python -m venv venv
- source venv/bin/activate  # Windows: venv\Scripts\activate
- pip install -r requirements.txt

### 3. Ajout de vos données (Important)
Le dossier `data_studio/` est vide pour respecter la confidentialité.
- **Ajoutez vos PDF** (manuels, doc technique) dans le dossier `data_studio/`.
- L'application scannera ces documents au premier lancement.

### 4. Lancement
- streamlit run app.py

---

## 🏗️ Architecture Technique
- **LangChain** : Orchestration du pipeline RAG.
- **ChromaDB** : Stockage des vecteurs sémantiques sur disque.
- **Mistral-7B** : Génération de réponses contextuelles via Ollama.

---

## 📝 À propos
Projet développé par **Lucas Delbecque** - Spécialisation IA appliquée aux studios d'animation.
