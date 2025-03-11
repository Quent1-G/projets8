import streamlit as st
import pandas as pd

# Charger la base de données
df_synthese_finale = pd.read_csv("Synthese_finale.csv")

def score_panier():
    """
    Cette fonction calcule :
    1. Le score moyen du panier en fonction des produits sélectionnés.
    2. Le score moyen des sous-groupes d'aliments correspondants.
    Puis les affiche sur des jauges pour :
    - "Score Statistique Standardisé"
    - "Score unique EF"
    """

    # Vérifier si le panier contient des produits
    if "panier" not in st.session_state or not st.session_state.panier:
        st.warning("Votre panier est vide.")
        return

    # Extraire les codes CIQUAL des produits du panier
    codes_ciqual_panier = [produit["code_ciqual"] for produit in st.session_state.panier]

    # Filtrer la base pour ne garder que les produits du panier
    df_panier = df_synthese_finale[df_synthese_finale["Code CIQUAL"].isin(codes_ciqual_panier)]

    if df_panier.empty:
        st.warning("Aucun produit du panier trouvé dans la base.")
        return

    # --- Jauge 1 : Score Statistique Standardisé ---
    if "Score Statistique Standardisé" in df_synthese_finale.columns:
        score_min = df_synthese_finale["Score Statistique Standardisé"].min()
        score_max = df_synthese_finale["Score Statistique Standardisé"].max()

        # Calcul du score moyen du panier
        score_moyen_panier = df_panier["Score Statistique Standardisé"].mean()

        # Calcul du score moyen des sous-groupes d'aliments
        scores_moyens_sous_groupes = df_synthese_finale.groupby("Sous-groupe d'aliment")["Score Statistique Standardisé"].mean()
        score_moyen_sous_groupes = scores_moyens_sous_groupes[df_panier["Sous-groupe d'aliment"].unique()].mean()

        st.subheader("📊 Score moyen du panier (Statistique Standardisé)")
        st.write(f"Score moyen : {score_moyen_panier:.2f} (Min: {score_min:.2f} - Max: {score_max:.2f})")
        st.slider("Score Statistique Standardisé", min_value=score_min, max_value=score_max, value=score_moyen_panier, disabled=True)

        st.subheader("📊 Score moyen pour ces types d'aliments")
        st.write(f"Score moyen des sous-groupes : {score_moyen_sous_groupes:.2f}")
        st.slider("Score Statistique Standardisé - Sous-groupes", min_value=score_min, max_value=score_max, value=score_moyen_sous_groupes, disabled=True)


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
