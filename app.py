import streamlit as st
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama

# Configuration des chemins
DATA_PATH = "./data_studio/"
CHROMA_PATH = "./chroma_db_storage"

st.set_page_config(page_title="Studio-Brain AI", page_icon="🎬")
st.title("Studio - AI Assistant")


# --- 1. GESTION DE LA PERSISTENCE ---

def clear_vdb():
    """Supprime le stockage de la base de données et vide le cache Streamlit."""
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    st.cache_resource.clear()
    st.success("Base de données réinitialisée ! Elle sera recréée au prochain scan.")


@st.cache_resource
def init_rag():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # Vérifier si la base existe déjà sur le disque
    if os.path.exists(CHROMA_PATH) and os.listdir(CHROMA_PATH):
        vectorstore = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings
        )
        st.sidebar.info("📂 Base de données chargée depuis le disque.")
    else:
        # Sinon, procéder à l'indexation initiale
        if not os.path.exists(DATA_PATH) or not os.listdir(DATA_PATH):
            st.error(f"Le dossier '{DATA_PATH}' est vide. Ajoute des PDF !")
            st.stop()

        st.sidebar.warning("⏳ Première indexation en cours (patience)...")
        loader = PyPDFDirectoryLoader(DATA_PATH)
        docs = loader.load()

        # Découpage optimisé pour la précision
        splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
        chunks = splitter.split_documents(docs)

        # Création et sauvegarde immédiate sur disque
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_PATH
        )
        st.sidebar.success("✅ Base créée et sauvegardée !")

    return vectorstore


# Initialisation
vectorstore = init_rag()

# --- 2. INTERFACE ET CHAT ---

with st.sidebar:
    st.header("Paramètres")
    if st.button("🔄 Réindexer les fichiers"):
        clear_vdb()
        st.rerun()

# Historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if prompt := st.chat_input("Pose une question technique..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Recherche sémantique (k=5 pour plus de contexte)
    relevant_docs = vectorstore.similarity_search(prompt, k=5)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    # Génération avec Mistral via Ollama
    with st.chat_message("assistant"):
        llm = ChatOllama(model="mistral")
        final_prompt = f"CONTEXTE TECHNIQUE:\n{context}\n\nQUESTION: {prompt}\n\nRéponds précisément."

        response = llm.invoke(final_prompt)
        full_response = response.content
        st.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})