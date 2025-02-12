import streamlit as st

# Appliquer du CSS pour forcer la pleine largeur
st.markdown(
    """
    <style>
        /* Forcer la largeur complète du contenu principal */
        .main-container {
            max-width: 100%;
            padding: 0;
            margin: 0;
        }
        /* Modifier la largeur de la page entière */
        .appview-container .main, .block-container {
            max-width: 100%;
            padding-left: 1rem;
            padding-right: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Fonction principale
def app():
    
    ########################################################################### Titre de la page principale######################################################################
    st.markdown("### Ce qu'on met dans nos assiettes, \n### quel impact sur la planète ?")

    ####################################################################### Bandeau latéral######################################################################
    st.sidebar.title("Contenu")
    st.sidebar.radio("Navigation", ["Accueil", "Contexte", "Méthodologie", "Analyse globale"])
    st.sidebar.write("### À propos")
    st.sidebar.write("Nous sommes des étudiants et bla bla bla...")

    ####################################################################### Contenu principal en pleine largeur######################################################################
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    st.write("""
    Aujourd'hui, bla bla bla, la consommation et la planète, bla bla bla.
    Ce projet explore l'impact de nos choix alimentaires sur l'environnement.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Lancer l'application
if __name__ == "__main__":
    app()
