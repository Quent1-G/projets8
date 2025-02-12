import streamlit as st

# Ajouter du CSS personnalisé
st.markdown(
    """
    <style>
    /* Style de la page principale */
    .main-content {
        padding: 20px;
        padding-left: 20px;
    }

    /* Style du bandeau latéral */
    .sidebar {
        position: fixed;
        top: 0;
        left: -250px;  /* Par défaut, le bandeau est caché */
        width: 250px;
        height: 100vh;
        background-color: #83ca69;
        overflow-y: auto;
        transition: left 0.3s ease;
        box-shadow: 2px 0px 5px rgba(0, 0, 0, 0.1);
        padding: 20px;
    }

    /* Style lorsque le bandeau latéral est visible */
    .sidebar.open {
        left: 0;  /* Afficher le bandeau */
    }

    /* Bouton pour ouvrir/fermer le bandeau */
    .toggle-btn {
        position: fixed;
        top: 20px;
        left: 20px;
        background-color: #83ca69;
        color: white;
        border: none;
        padding: 10px;
        font-size: 16px;
        cursor: pointer;
        z-index: 100;
    }

    </style>
    """, unsafe_allow_html=True
)

# Interface de la page principale
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Titre de la page
st.title("Page vide avec bandeau latéral défilant et refermable")

# Ajouter un bouton pour ouvrir/fermer le bandeau
if 'sidebar_open' not in st.session_state:
    st.session_state.sidebar_open = False

# Fonction pour ouvrir/fermer le bandeau
def toggle_sidebar():
    st.session_state.sidebar_open = not st.session_state.sidebar_open

# Ajouter le bouton de toggle
st.markdown(f"""
    <button class="toggle-btn" onclick="toggle_sidebar()">{'Ouvrir' if not st.session_state.sidebar_open else 'Fermer'} le bandeau</button>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Interface du bandeau latéral (référencé via l'état pour l'affichage)
st.markdown(
    f"""
    <div class="sidebar {'open' if st.session_state.sidebar_open else ''}">
        <h2>Menu du Bandeau Latéral</h2>
        <p>Ce bandeau peut être défilé et refermé à votre convenance.</p>
    </div>
    """, unsafe_allow_html=True
)
