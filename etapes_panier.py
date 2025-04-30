import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

@st.cache_data
def charger_bdd():
    return pd.read_csv("agribalyse-31-detail-par-etape.csv")

def etapes_panier():
    st.header("Analyse des étapes du panier")

    # Vérification du panier
    if "panier" not in st.session_state or not st.session_state.panier:
        st.warning("Ajoutez des produits pour voir l'analyse.")
        return

    codes_ciqual_panier = [int(produit["code_ciqual"]) for produit in st.session_state.panier]

    # Charger la BDD étapes
    df_agribalyse = charger_bdd()

    if "Code CIQUAL" not in df_agribalyse.columns:
        st.error("Erreur : La colonne 'Code CIQUAL' est introuvable dans la BDD.")
        return

    # Filtrer la BDD pour ne garder que les produits du panier
    df_panier = df_agribalyse[df_agribalyse["Code CIQUAL"].isin(codes_ciqual_panier)]

    if df_panier.empty:
        st.warning("Aucun des produits du panier ne correspond à la BDD étapes.")
        return

    # Sélection de l'étape
    etapes = ["Agriculture", "Transformation", "Emballage", "Transport", "Supermarché et distribution", "Consommation"]
    
    # Sélection de la variable à comparer dans le radar
    variables_disponibles = df_agribalyse.columns
    variable_selectionnee = st.selectbox("Sélectionnez une variable pour le radar", variables_disponibles)

    # Filtrer les colonnes contenant l'étape sélectionnée
    colonnes_etape = [col for col in df_agribalyse.columns if any(etape in col for etape in etapes)]
    
    # Centrage et réduction des données
    def centrer_reduire(df, colonnes):
        df_normalise = df.copy()
        for col in colonnes:
            mean = df[col].mean()
            std = df[col].std()
            df_normalise[col] = (df[col] - mean) / std  # Centrer et réduire
        return df_normalise

    # Normalisation du panier et du panier moyen
    df_panier_normalise = centrer_reduire(df_panier[colonnes_etape], colonnes_etape)

    # Calcul des moyennes des sous-groupes pour les étapes
    moyennes_sous_groupes = df_agribalyse.groupby("Sous-groupe d'aliment")[colonnes_etape].mean()

    # Calcul de la moyenne des sous-groupes pour chaque étape
    panier_moyen_normalise = moyennes_sous_groupes[variable_selectionnee].mean()

    # --------------------------
    # 🔽 Graphique radar comparatif
    # --------------------------

    # Données du panier de l'utilisateur et du panier moyen
    valeurs_panier = []
    valeurs_panier_moyenne = []

    for etape in etapes:
        # Filtrer les colonnes pour chaque étape
        colonnes_etape = [col for col in df_agribalyse.columns if etape in col]

        if not colonnes_etape:
            continue
        
        # Normaliser les valeurs de la variable sélectionnée pour chaque étape
        df_panier_etape_normalise = centrer_reduire(df_panier[colonnes_etape], colonnes_etape)
        valeurs_panier.append(df_panier_etape_normalise[variable_selectionnee].mean())
        
        # Moyenne des sous-groupes pour cette étape
        moyennes_etape = moyennes_sous_groupes[variable_selectionnee]
        valeurs_panier_moyenne.append(moyennes_etape.mean())

    # Ajouter les données au graphique radar
    fig = go.Figure()

    # Ajouter les données du panier utilisateur
    fig.add_trace(go.Scatterpolar(
        r=valeurs_panier,
        theta=etapes,
        fill='toself',
        name="Panier Utilisateur"
    ))

    # Ajouter les données du panier moyen
    fig.add_trace(go.Scatterpolar(
        r=valeurs_panier_moyenne,
        theta=etapes,
        fill='toself',
        name="Panier Moyen"
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[-1, 1]  # Car centré et réduit
            )
        ),
        title=f"Comparaison des paniers pour la variable '{variable_selectionnee}'",
        showlegend=True
    )

    st.plotly_chart(fig)

    # Affichage des résultats supplémentaires
    st.subheader(f"Analyse des étapes pour la variable : {variable_selectionnee}")

    # Calcul et affichage des sommes des valeurs du panier et des moyennes des sous-groupes pour chaque étape
    somme_valeurs_panier = df_panier[colonnes_etape].sum().sum()
    somme_moyennes_sous_groupes = sum(moyennes_sous_groupes.loc[sous_groupe].sum() for sous_groupe in df_panier["Sous-groupe d'aliment"])

    st.write(f"🔹 **Somme des valeurs du panier** : {somme_valeurs_panier:.2f}")
    st.write(f"🔹 **Somme des moyennes des sous-groupes** : {somme_moyennes_sous_groupes:.2f}")
