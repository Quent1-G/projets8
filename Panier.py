import streamlit as st
import pandas as pd

# Charger la base de données
df_synthese_finale = pd.read_csv("Synthese_finale.csv")

# Initialiser le panier
if "panier" not in st.session_state:
    st.session_state.panier = []

# Initialiser le produit sélectionné
if "produit_selectionne" not in st.session_state:
    st.session_state.produit_selectionne = None

st.title("🛍️ Gestion du Panier")

# Barre de recherche + Liste déroulante
search_query = st.text_input("🔍 Recherchez un produit par nom")

produit_selectionne = None  # Variable temporaire pour éviter l'ajout automatique

if search_query:
    produits_trouves = df_synthese_finale[df_synthese_finale["Nom du Produit en Français"].str.contains(search_query, case=False, na=False)]
    
    if not produits_trouves.empty:
        produit_selectionne = st.selectbox("📌 Sélectionnez un produit :", [""] + list(produits_trouves["Nom du Produit en Français"].unique()))

# Ajouter au panier uniquement si un produit est sélectionné et que l'utilisateur clique sur le bouton
if produit_selectionne and produit_selectionne != "":
    code_ciqual = df_synthese_finale[df_synthese_finale["Nom du Produit en Français"] == produit_selectionne]["Code CIQUAL"].values[0]

    if st.button("➕ Ajouter au panier"):
        if not any(p["nom"] == produit_selectionne for p in st.session_state.panier):
            st.session_state.panier.append({"nom": produit_selectionne, "code_ciqual": code_ciqual})
            st.success(f"✅ {produit_selectionne} ajouté au panier.")
            st.rerun()
        else:
            st.warning(f"⚠️ {produit_selectionne} est déjà dans le panier.")

# Affichage du panier
st.subheader("📦 Votre panier")
if st.session_state.panier:
    for index, item in enumerate(st.session_state.panier):
        col1, col2 = st.columns([4, 1])
        col1.write(f"🔹 **{item['nom']}** (Code CIQUAL : {item['code_ciqual']})")
        
        # Bouton pour supprimer un produit
        if col2.button("❌", key=f"remove_{index}"):
            st.session_state.panier.pop(index)
            st.rerun()
else:
    st.info("🛒 Votre panier est vide.")
