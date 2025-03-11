import streamlit as st
import pandas as pd

# Charger la base de données
df_synthese_finale = pd.read_csv("Synthese_finale.csv")

def score_panier():
    """
    Cette fonction calcule le score moyen du panier pour deux critères :
    - "Score Statistique Standardisé"
    - "Score unique EF"
    Puis les affiche sur des jauges avec leurs vraies valeurs.
    """
    # Vérifier si le panier contient des produits
    if "panier" not in st.session_state or not st.session_state.panier:
        st.warning("Votre panier est vide.")
        return

    # Extraire les codes CIQUAL des produits du panier
    codes_ciqual_panier = [produit["code_ciqual"] for produit in st.session_state.panier]

    # --- Jauge 1 : Score Statistique Standardisé ---
    if "Score Statistique Standardisé" in df_synthese_finale.columns:
        score_min = df_synthese_finale["Score Statistique Standardisé"].min()
        score_max = df_synthese_finale["Score Statistique Standardisé"].max()

        scores_panier = df_synthese_finale[df_synthese_finale["Code CIQUAL"].isin(codes_ciqual_panier)]["Score Statistique Standardisé"]

        if not scores_panier.empty:
            score_moyen = scores_panier.mean()

            st.subheader("📊 Score moyen du panier (Statistique Standardisé)")
            st.write(f"Score moyen : {score_moyen:.2f} (Min: {score_min:.2f} - Max: {score_max:.2f})")

            # Affichage de la jauge avec valeur réelle
            st.slider("Score Statistique Standardisé", min_value=score_min, max_value=score_max, value=score_moyen, disabled=True)
        else:
            st.warning("Aucun score trouvé pour 'Score Statistique Standardisé'.")

    # --- Jauge 2 : Score unique EF ---
    if "Score unique EF" in df_synthese_finale.columns:
        score_ef_min = df_synthese_finale["Score unique EF"].min()
        score_ef_max = df_synthese_finale["Score unique EF"].max()

        scores_ef_panier = df_synthese_finale[df_synthese_finale["Code CIQUAL"].isin(codes_ciqual_panier)]["Score unique EF"]

        if not scores_ef_panier.empty:
            score_ef_moyen = scores_ef_panier.mean()

            st.subheader("🌍 Score Environnemental (Score unique EF)")
            st.write(f"Score EF moyen : {score_ef_moyen:.2f} (Min: {score_ef_min:.2f} - Max: {score_ef_max:.2f})")

            # Affichage de la jauge avec valeur réelle
            st.slider("Score unique EF", min_value=score_ef_min, max_value=score_ef_max, value=score_ef_moyen, disabled=True)
        else:
            st.warning("Aucun score trouvé pour 'Score unique EF'.")
