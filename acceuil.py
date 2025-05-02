import streamlit as st

st.set_page_config(
    page_title="Accueil",
    page_icon="🏠",
    layout="wide"
)

st.title("Bienvenue sur notre site Streamlit !")
st.write("Ceci est la page d'accueil.")

if st.button("Aller à l'application principale"):
    st.switch_page("main.py")  # Assure-toi que main.py existe
