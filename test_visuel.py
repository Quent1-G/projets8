import streamlit as st

# Fonction principale de l'application
def app():
    # Ajout du titre de la page principale
    st.title("Page Principale")
    st.write("Voici la partie principale de la page.")

    # Contenu du bandeau latéral avec un bouton pour ouvrir/fermer
    with st.sidebar:
        st.title("Bandeau Latéral")
        bandeau_ouvert = st.checkbox("Ouvrir le bandeau", value=True)
        
        if bandeau_ouvert:
            st.subheader("Bienvenue dans le bandeau !")
            st.write("Tu peux mettre des options, des informations ou des graphiques ici.")

    # Ajoute du contenu supplémentaire à la page principale
    st.write("Tu peux également ajouter plus de contenu ici, en dehors du bandeau.")
    st.write("N'oublie pas que le bandeau latéral est complètement interactif.")
