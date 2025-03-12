import streamlit as st
from pathlib import Path
import base64

# Configuration de la page
st.set_page_config(
    page_title='Mon Application Streamlit',
    layout="wide",
    initial_sidebar_state="expanded",
)

def img_to_bytes(img_path):
    """Convertir une image en base64"""
    img_bytes = Path(img_path).read_bytes()
    return base64.b64encode(img_bytes).decode()

def sidebar():
    """Créer le menu latéral"""
    st.sidebar.markdown('''[<img src='data:image/png;base64,{}' width=32 height=32>](https://streamlit.io/)'''.format(img_to_bytes("logomark_website.png")), unsafe_allow_html=True)
    st.sidebar.header('Menu')
    st.sidebar.markdown("""Application personnalisée avec Streamlit""")
    
    st.sidebar.markdown('__Navigation__')
    option = st.sidebar.radio("Choisissez une page:", ["Accueil", "Données", "Paramètres"])
    return option

def accueil():
    """Page d'accueil"""
    st.title("Bienvenue sur mon application Streamlit")
    st.write("Cette application utilise un bandeau latéral pour la navigation.")

def donnees():
    """Affichage des données"""
    st.title("Données Agribalyse")
    df = st.file_uploader("Téléchargez un fichier CSV", type=["csv"])
    if df is not None:
        st.dataframe(df)

def parametres():
    """Page des paramètres"""
    st.title("Paramètres")
    couleur = st.color_picker("Choisissez une couleur de thème", "#FF5733")
    st.write(f"Couleur sélectionnée : {couleur}")

def main():
    page = sidebar()
    if page == "Accueil":
        accueil()
    elif page == "Données":
        donnees()
    elif page == "Paramètres":
        parametres()

if __name__ == '__main__':
    main()
