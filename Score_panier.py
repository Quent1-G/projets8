import streamlit as st
import pandas as pd

# Charger la base de données
df_synthese_finale = pd.read_csv("Synthese_finale.csv")

def score_panier():
    """
    Cette fonction calcule le score du panier en fonction des scores des produits et affiche une jauge.
    """
    # Centrer les scores de la BDD entière
    score_min, score_max = df_synthese_finale["Score Normalisé"].min(), df_synthese_finale["Score Normalisé"].max()
    df_synthese_finale["Score Centré"] = 2.5 + (df_synthese_finale["Score Normalisé"] - (score_min + score_max) / 2) * 5 / (score_max - score_min)
    df_synthese_finale["Score Centré"] = df_synthese_finale["Score Centré"].clip(0, 5)

    # Extraire les codes CIQUAL des produits du panier
    codes_ciqual_panier = [produit["code_ciqual"] for produit in st.session_state.panier]

    # Filtrer les scores des produits du panier
    scores_panier = df_synthese_finale[df_synthese_finale["Code CIQUAL"].isin(codes_ciqual_panier)]["Score Centré"]

    # Calculer la moyenne des scores
    if not scores_panier.empty:
        score_moyen = scores_panier.mean()
    else:
        score_moyen = 0
        st.warning("Aucun score trouvé pour les produits dans le panier.")

    # Affichage de la jauge avec le score moyen
    st.subheader("📊 Score moyen du panier")
    st.write(f"Score moyen centré du panier : {score_moyen:.2f}/5")

    # Affichage de la jauge
    st.progress(score_moyen / 5)  # La jauge va de 0 à 1, donc on divise le score par 5
