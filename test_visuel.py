import streamlit as st

# Ajouter du CSS personnalisé
st.markdown(
    """
    <style>
    /* Définir un fond et un padding pour la page principale */
    .main-content {
        margin-left: 250px;  /* Espace pour le bandeau latéral */
        padding: 20px;
        overflow-y: scroll;  /* Permet à la page principale d'être défilable */
        height: 100vh;  /* Remplir l'écran */
    }

    /* Style du bandeau latéral (fixe sur le côté gauche) */
    .sidebar {
        position: fixed;
        top: 0;
        left: 0;
        width: 250px;  /* Largeur du bandeau */
        height: 100vh;  /* Hauteur maximale pour occuper toute la hauteur */
        background-color: #f0f2f6;  /* Couleur de fond du bandeau */
        overflow-y: auto;  /* Permet au bandeau d'être défilable */
        padding: 20px;
        box-shadow: 2px 0px 5px rgba(0, 0, 0, 0.1);  /* Ajoute une ombre pour le contraste */
    }

    /* Style du contenu du bandeau latéral */
    .sidebar .stSidebar > div {
        padding: 20px;
        font-size: 18px;
    }

    </style>
    """, unsafe_allow_html=True
)

# Interface principale
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Titre de la page principale
st.title("Mon Application Streamlit avec Bandeau Latéral Défilant")

# Exemple de contenu sur la page principale
st.write("Voici le contenu de la page principale qui peut être défilé.")
st.write("Ajoutez du contenu ici, des graphiques, des tableaux, etc.")

for i in range(30):
    st.write(f"Exemple de contenu {i+1}")

st.markdown('</div>', unsafe_allow_html=True)

# Interface du bandeau latéral
st.sidebar.markdown('<div class="sidebar">', unsafe_allow_html=True)

# Contenu du bandeau latéral
st.sidebar.title("Options de Menu")
st.sidebar.radio("Choisissez une option", ["Option 1", "Option 2", "Option 3"])
st.sidebar.write("Plus de détails ici...")

st.sidebar.markdown('</div>', unsafe_allow_html=True)
