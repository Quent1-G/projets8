import streamlit as st

# Ajouter du CSS personnalisé pour la mise en page
st.markdown(
    """
    <style>
    /* Style du bandeau latéral */
    .sidebar .sidebar-content {
        padding: 20px;
        font-size: 18px;
    }
    /* Style du contenu de la page principale */
    .main-content {
        margin-left: 250px;  /* Espace réservé pour le bandeau latéral */
        padding: 20px;
        overflow-y: auto;  /* Permet de défiler dans la page principale */
        height: 100vh;  /* Hauteur de la fenêtre pour occuper tout l'écran */
    }
    /* Style du bandeau latéral */
    .stSidebar {
        position: fixed;
        top: 0;
        left: 0;
        width: 250px;  /* Largeur du bandeau latéral */
        height: 100vh;  /* Hauteur du bandeau pour qu'il occupe toute la hauteur de la page */
        background-color: #f0f2f6;
        overflow-y: auto;
        box-shadow: 2px 0px 5px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True
)

# Contenu principal de la page
st.markdown('<div class="main-content">', unsafe_allow_html=True)
# Titre de la page principale
st.title("Mon Application Streamlit avec Bandeau Latéral Défilant")

# Exemple de contenu dans la page principale
st.write("Voici le contenu de la page principale qui peut être défilé.")
st.write("Ajoutez du contenu ici, des graphiques, des tableaux, etc.")
for i in range(30):
    st.write(f"Exemple de contenu {i+1}")

# Fin du contenu principal
st.markdown('</div>', unsafe_allow_html=True)

# Contenu du bandeau latéral
st.sidebar.title("Options de Menu")
st.sidebar.radio("Choisissez une option", ["Option 1", "Option 2", "Option 3"])
st.sidebar.write("Plus de détails ici...")
