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
    st.markdown("<h1 style='margin-bottom: 0; padding-bottom: 0;'>Ce qu'on met dans nos assiettes...</h1><h1 style='margin-top: 0; padding-top: 0;'>Quel impact sur la planète ?</h1>", unsafe_allow_html=True)
    
    ####################################################################### Bandeau latéral######################################################################
    st.sidebar.title("Contenu")
    st.sidebar.radio("Navigation", ["Accueil", "Contexte", "Méthodologie", "Analyse globale"])
    st.sidebar.write("### À propos")
    st.sidebar.write("Nous sommes des étudiants et bla bla bla...")

    ####################################################################### Contenu principal en pleine largeur######################################################################
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.write("Explorez l'impact environnemental de votre alimentation")
    st.write("""
        Aujourd’hui, la consommation alimentaire a un impact environnemental croissant. 
        Il est donc essentiel de mieux comprendre les effets de nos choix alimentaires. 
        Grâce à l’Analyse du Cycle de Vie (ACV) et aux données d'Agribalyse, nous vous proposons un outil interactif pour explorer l’empreinte écologique de votre panier alimentaire.
        
        ### Ce site vous permet de :
        - **Rechercher** des aliments et constituer votre panier personnalisé.
        - **Accéder** aux impacts environnementaux de chaque aliment ainsi qu'à l’empreinte globale de votre panier.
        - **Découvrir** les détails des ingrédients ou des étapes de production les plus impactantes.
        - **Explorer** un regroupement des aliments basé sur une analyse en composantes principales.
        - **Profiter** d’un **nouveau score** développé pour évaluer l’impact environnemental des aliments de manière globale et compréhensible.
        
        🌱 **Faites des choix éclairés et responsables pour une alimentation plus durable !**
        """)
    st.markdown('</div>', unsafe_allow_html=True)

# Lancer l'application
if __name__ == "__main__":
    app()
