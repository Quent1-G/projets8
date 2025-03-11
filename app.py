import streamlit as st
from Panier import gerer_panier
from Score_panier import score_panier

# Appeler la fonction qui gère tout le panier
gerer_panier()

# Affichage des codes CIQUAL dans le panier
codes_ciqual = [int(produit["code_ciqual"]) for produit in st.session_state.panier]


# Appeler la fonction pour calculer le score du panier
score_panier()
