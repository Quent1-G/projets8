import streamlit as st
from Panier import gerer_panier

# Appeler la fonction qui gère tout le panier
gerer_panier()
# Affichage des codes CIQUAL dans le panier
codes_ciqual = [produit["code_ciqual"] for produit in st.session_state.panier]
if codes_ciqual:
  st.write("Liste des codes CIQUAL dans le panier :", codes_ciqual)
else:
  st.write("Il n'y a pas de codes CIQUAL dans le panier.")
