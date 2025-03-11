import pandas as pd
import streamlit as st

# Charger la base de données
@st.cache_data
def charger_donnees():
    return pd.read_csv("Synthese_finale.csv")

df_synthese_finale = charger_donnees()

# Titre de l'application
st.title("🛒 Panier d'Achat - Sélection de Produits")

# Saisie utilisateur - Barre de recherche
recherche = st.text_input("🔍 Rechercher un produit :")

# Initialiser le panier dans la session Streamlit
if "panier" not in st.session_state:
    st.session_state.panier = []

# Filtrer les produits correspondant
if recherche:
    resultats = df_synthese_finale[df_synthese_finale["Nom du Produit en Français"].str.contains(recherche, case=False, na=False)]
    
    if not resultats.empty:
        # Sélectionner un produit via un menu déroulant
        choix = st.selectbox("📌 Sélectionnez un produit :", resultats["Nom du Produit en Français"])
        
        # Ajouter au panier
        if st.button("➕ Ajouter au panier"):
            produit_selectionne = df_synthese_finale[df_synthese_finale["Nom du Produit en Français"] == choix].iloc[0]
            
            # Vérifier si le produit est déjà dans le panier
            deja_present = any(p['Nom du Produit en Français'] == choix for p in st.session_state.panier)
            
            if not deja_present:
                st.session_state.panier.append(produit_selectionne.to_dict())
                st.success(f"✅ {choix} ajouté au panier !")
            else:
                st.warning(f"⚠️ {choix} est déjà dans le panier.")
    else:
        st.write("❌ Aucun produit trouvé.")

# Affichage du panier
st.subheader("🛍️ Votre Panier")

if st.session_state.panier:
    for i, produit in enumerate(st.session_state.panier):
        st.write(f"**{produit['Nom du Produit en Français']}** - Code Ciqual : {produit['Code CIQUAL']}")
        
        # Supprimer un produit du panier
        if st.button(f"🗑️ Supprimer {produit['Nom du Produit en Français']}", key=f"suppr_{i}"):
            st.session_state.panier.pop(i)
            st.experimental_rerun()
else:
    st.write("📭 Votre panier est vide.")
