import streamlit as st
import pandas as pd

# Charger la base de données
df_synthese_finale = pd.read_csv("Synthese_finale.csv")

def score_panier():
    """
    Cette fonction calcule le score du panier en fonction des scores des produits et affiche une jauge.
    """
    # Vérifier si le panier contient des produits
    if "panier" not in st.session_state or not st.session_state.panier:
        st.warning("Votre panier est vide.")
        return

    # Déterminer les scores min et max pour l'affichage de la jauge
    score_min = df_synthese_finale["Score Statistique Standardisé"].min()
    score_max = df_synthese_finale["Score Statistique Standardisé"].max()

    # Extraire les codes CIQUAL des produits du panier
    codes_ciqual_panier = [produit["code_ciqual"] for produit in st.session_state.panier]

    # Filtrer les scores des produits du panier
    scores_panier = df_synthese_finale[df_synthese_finale["Code CIQUAL"].isin(codes_ciqual_panier)]["Score Statistique Standardisé"]

    # Calculer la moyenne des scores
    if not scores_panier.empty:
        score_moyen = scores_panier.mean()
    else:
        score_moyen = None

    # Affichage de la jauge
    st.subheader("📊 Score moyen du panier")

    if score_moyen is not None:
        st.write(f"Score moyen du panier : {score_moyen:.2f}")

        # Normaliser le score entre 0 et 1 pour la jauge
        score_normalisé = (score_moyen - score_min) / (score_max - score_min)

        # Afficher une jauge
        st.progress(score_normalisé)  # Progress prend une valeur entre 0 et 1
    else:
        st.warning("Aucun score trouvé pour les produits dans le panier.")
