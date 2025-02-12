import streamlit as st

# Fonction principale pour l'application
def app():
    # Titre de la page principale
    st.title("Mon Application Streamlit avec Bandeau Latéral Défilant")

    # Créer une mise en page avec un conteneur de deux colonnes
    col1, col2 = st.columns([1, 4])  # col1 pour le bandeau, col2 pour le contenu principal

    # Contenu du bandeau latéral
    with col1:
        st.sidebar.title("Options de Menu")
        st.sidebar.radio("Choisissez une option", ["Option 1", "Option 2", "Option 3"])
        st.sidebar.write("Plus de détails ici...")

    # Contenu principal de la page
    with col2:
        st.write("Voici le contenu de la page principale qui peut être défilé.")
        st.write("Ajoutez du contenu ici, des graphiques, des tableaux, etc.")
        for i in range(30):
            st.write(f"Exemple de contenu {i+1}")

# Lancer l'application
if __name__ == "__main__":
    app()
