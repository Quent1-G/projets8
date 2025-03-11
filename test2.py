Panier.py

# Créer une liste des codes CIQUAL
codes_ciqual = [produit["code_ciqual"] for produit in st.session_state.panier]

# Afficher la liste des codes CIQUAL
st.write("Liste des codes CIQUAL dans le panier :", codes_ciqual)
