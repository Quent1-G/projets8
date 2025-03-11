import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Charger la base de données
df_synthese_finale = pd.read_csv("Synthese_finale.csv")

def score_panier():
    """
    Cette fonction calcule :
    1. Le score moyen du panier en fonction des produits sélectionnés.
    2. Le score moyen des sous-groupes d'aliments correspondants.
    Puis les affiche sur une jauge avec 2 points légendés pour :
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

    # --- Jauge combinée pour "Score Statistique Standardisé" et "Score moyen pour ces types d'aliments" ---
    if "Score Statistique Standardisé" in df_synthese_finale.columns:
        score_min = df_synthese_finale["Score Statistique Standardisé"].min()
        score_max = df_synthese_finale["Score Statistique Standardisé"].max()

        # Calcul du score moyen du panier
        score_moyen_panier = df_panier["Score Statistique Standardisé"].mean()

        # Calcul du score moyen des sous-groupes d'aliments
        scores_moyens_sous_groupes = df_synthese_finale.groupby("Sous-groupe d'aliment")["Score Statistique Standardisé"].mean()
        score_moyen_sous_groupes = scores_moyens_sous_groupes[df_panier["Sous-groupe d'aliment"].unique()].mean()

        st.subheader("📊 Score Statistique Standardisé et Score moyen pour ces types d'aliments")

        # Création de la jauge avec Plotly
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score_moyen_panier,
            delta={'reference': score_moyen_sous_groupes},
            gauge={
                'axis': {'range': [score_min, score_max]},
                'steps': [
                    {'range': [score_min, score_max], 'color': "lightgray"}
                ],
                'bar': {'color': "blue"},
            },
            title={'text': "Score Statistique Standardisé"},
            annotations=[
                {"x": 0.25, "y": 0.8, "text": f"Panier: {score_moyen_panier:.2f}", "showarrow": True, "arrowhead": 4},
                {"x": 0.75, "y": 0.8, "text": f"Sous-groupes: {score_moyen_sous_groupes:.2f}", "showarrow": True, "arrowhead": 4}
            ]
        ))

        st.plotly_chart(fig)

    # --- Jauge combinée pour "Score unique EF" et "Score moyen pour ces types d'aliments" ---
    if "Score unique EF" in df_synthese_finale.columns:
        score_ef_min = df_synthese_finale["Score unique EF"].min()
        score_ef_max = df_synthese_finale["Score unique EF"].max()

        # Calcul du score EF moyen du panier
        score_ef_moyen_panier = df_panier["Score unique EF"].mean()

        # Calcul du score EF moyen des sous-groupes d'aliments
        scores_ef_moyens_sous_groupes = df_synthese_finale.groupby("Sous-groupe d'aliment")["Score unique EF"].mean()
        score_ef_moyen_sous_groupes = scores_ef_moyens_sous_groupes[df_panier["Sous-groupe d'aliment"].unique()].mean()

        st.subheader("🌍 Score Environnemental (Score unique EF) et Score moyen pour ces types d'aliments")

        # Création de la jauge avec Plotly
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score_ef_moyen_panier,
            delta={'reference': score_ef_moyen_sous_groupes},
            gauge={
                'axis': {'range': [score_ef_min, score_ef_max]},
                'steps': [
                    {'range': [score_ef_min, score_ef_max], 'color': "lightgray"}
                ],
                'bar': {'color': "green"},
            },
            title={'text': "Score Environnemental"},
            annotations=[
                {"x": 0.25, "y": 0.8, "text": f"Panier: {score_ef_moyen_panier:.2f}", "showarrow": True, "arrowhead": 4},
                {"x": 0.75, "y": 0.8, "text": f"Sous-groupes: {score_ef_moyen_sous_groupes:.2f}", "showarrow": True, "arrowhead": 4}
            ]
        ))

        st.plotly_chart(fig)
