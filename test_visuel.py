import streamlit as st

# Ajouter du CSS pour forcer le contenu principal en pleine largeur
st.markdown(
    """
    <style>
        .main-container {
            max-width: 95%;  /* Utiliser presque toute la largeur */
            padding: 0 5%;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Fonction principale
def app():
    # Titre de la page principale
    st.title("Ce qu'on met dans nos assiettes, quel impact sur la planète ?")

    # Bandeau latéral
    st.sidebar.title("Contenu")
    st.sidebar.radio("Navigation", ["Accueil", "Contexte", "Méthodologie", "Analyse globale"])
    st.sidebar.write("### À propos")
    st.sidebar.write("Nous sommes des étudiants et bla bla bla...")

    # Contenu principal dans un conteneur avec la classe CSS ajoutée
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    st.write("""
    Aujourd'hui, bla bla bla, la consommation et la planète, bla bla bla.
    Ce projet explore l'impact de nos choix alimentaires sur l'environnement.
    """)

    # Ajouter plus de contenu pour tester le défilement
    for i in range(30):
        st.write(f"Paragraphe d'exemple {i+1}")

    st.markdown('</div>', unsafe_allow_html=True)

# Lancer l'application
if __name__ == "__main__":
    app()
