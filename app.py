import streamlit as st
import openai
import os
from PIL import Image

# ─────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────

# Clé API
openai.api_key = st.secrets["openai_api_key"] if "openai_api_key" in st.secrets else os.getenv("OPENAI_API_KEY")

# Titre de la page
st.set_page_config(page_title="Assistant Administratif - Guinée", page_icon="🇬🇳")

# Afficher le logo en haut
logo_path = "image.jpeg"  # Le nom de l'image uploadée
if os.path.exists(logo_path):
    image = Image.open(logo_path)
    st.image(image, width=200)

# Titre
st.markdown("<h1 style='text-align: center;'>🇬🇳 Assistant Administratif Guinéen</h1>", unsafe_allow_html=True)
st.write("Pose ta question sur une démarche administrative en Guinée. Tu recevras une réponse claire et adaptée à la réalité locale.")

# ─────────────────────────────────────────────────────
# INPUT UTILISATEUR
# ─────────────────────────────────────────────────────

question = st.text_area("❓ Ta question :", placeholder="Ex : Comment obtenir un passeport en Guinée ?")
go = st.button("🔍 Obtenir de l'aide")

# ─────────────────────────────────────────────────────
# PROMPT SYSTEME (personnalisation du comportement du LLM)
# ─────────────────────────────────────────────────────

SYSTEM_PROMPT = """
Tu es un assistant administratif guinéen. Ton rôle est d’expliquer simplement aux citoyens comment effectuer des démarches administratives en République de Guinée.

Ta réponse doit inclure :
- Les **étapes à suivre**
- Les **documents nécessaires**
- Les **lieux où aller** (avec exemples en Guinée)
- Et les **coûts approximatifs** si connus.

Utilise un langage **accessible**, clair et sans jargon technique.
"""

# ─────────────────────────────────────────────────────
# APPEL API OpenAI (format 1.x.x)
# ─────────────────────────────────────────────────────

if go and question.strip():
    with st.spinner("Consultation de l’administration guinéenne…"):
        try:
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=800
            )
            answer = response.choices[0].message.content
            st.success("Voici les informations utiles 👇")
            st.markdown(answer)
        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")
else:
    st.info("Pose une question puis clique sur le bouton ci-dessus.")
