import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def charger_bdd():
    return pd.read_csv("agribalyse-31-detail-par-etape.csv")

def etapes_panier():
    st.header("Analyse des étapes du panier")

    if "panier" not in st.session_state or not st.session_state.panier:
        st.warning("Ajoutez des produits pour voir l'analyse.")
        return

    codes_ciqual_panier = [int(produit["code_ciqual"]) for produit in st.session_state.panier]

    df_agribalyse = charger_bdd()

    if "Code CIQUAL" not in df_agribalyse.columns:
        st.error("Erreur : La colonne 'Code CIQUAL' est introuvable dans la BDD.")
        return

    df_panier = df_agribalyse[df_agribalyse["Code CIQUAL"].isin(codes_ciqual_panier)]

    if df_panier.empty:
        st.warning("Aucun des produits du panier ne correspond à la BDD étapes.")
        return

    etapes = ["Agriculture", "Transformation", "Emballage", "Transport", "Supermarché et distribution", "Consommation"]

    # === DIAGRAMME EN ÉTOILE : "Score unique EF" sur toutes les étapes ===
    st.subheader("Score unique EF par étape (diagramme en étoile)")

    valeurs_panier = {}
    moyennes_sous_groupes = {}

    for etape in etapes:
        colonnes_score_ef = [col for col in df_agribalyse.columns if etape in col and "Score unique EF" in col]

        if not colonnes_score_ef:
            continue

        df_panier[colonnes_score_ef] = df_panier[colonnes_score_ef].apply(pd.to_numeric, errors="coerce")
        df_agribalyse[colonnes_score_ef] = df_agribalyse[colonnes_score_ef].apply(pd.to_numeric, errors="coerce")

        # Moyenne directe du panier
        moyenne_panier = df_panier[colonnes_score_ef].mean().mean()
        valeurs_panier[etape] = moyenne_panier

        # Moyenne pondérée par sous-groupes
        sous_groupes_panier = df_panier["Sous-groupe d'aliment"]
        moyennes = df_agribalyse.groupby("Sous-groupe d'aliment")[colonnes_score_ef].mean()

        total = 0
        count = 0
        for sous_groupe in sous_groupes_panier:
            if sous_groupe in moyennes.index:
                total += moyennes.loc[sous_groupe].mean()
                count += 1

        moyenne_sous_groupes = total / count if count > 0 else 0
        moyennes_sous_groupes[etape] = moyenne_sous_groupes

    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=list(valeurs_panier.values()),
        theta=list(valeurs_panier.keys()),
        fill='toself',
        name="Votre Panier"
    ))

    fig_radar.add_trace(go.Scatterpolar(
        r=list(moyennes_sous_groupes.values()),
        theta=list(moyennes_sous_groupes.keys()),
        fill='toself',
        name="Panier moyen similaire"
    ))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True,
        title="Comparaison de votre panier avec le panier moyen similaire - Score EF"
    )

    st.plotly_chart(fig_radar)

    # === ANALYSE DÉTAILLÉE PAR ÉTAPE + INDICATEUR (ton code existant + nouvelle fonctionnalité en dessous) ===
    st.subheader("Analyse détaillée par étape et indicateur")

    etape_selectionnee = st.selectbox("Étape à afficher :", etapes)

    impacts = [
        'Score unique EF', 'Changement climatique', 'Appauvrissement de la couche d\'ozone',
        'Rayonnements ionisants', 'Formation photochimique d\'ozone', 'Particules fines - Agriculture',
        'Effets toxicologiques sur la santé humaine : substances non-cancérogènes',
        'Effets toxicologiques sur la santé humaine : substances cancérogènes',
        'Acidification terrestre et eaux douces', 'Eutrophisation eaux douces',
        'Eutrophisation marine', 'Eutrophisation terrestre',
        'Écotoxicité pour écosystèmes aquatiques d\'eau douce', 'Utilisation du sol',
        'Épuisement des ressources eau', 'Épuisement des ressources énergétiques',
        'Épuisement des ressources minéraux', 'Changement climatique - émissions biogéniques',
        'Changement climatique - émissions fossiles',
        'Changement climatique - émissions liées au changement d\'affectation des sols'
    ]

    unites = {
        'Score unique EF': 'sans unité',
        'Changement climatique': 'kg CO2 eq/kg',
        'Appauvrissement de la couche d\'ozone': 'kg CVC11 eq/kg',
        'Rayonnements ionisants': 'kBq U-235 eq/kg',
        'Formation photochimique d\'ozone': 'kg NMVOC eq/kg',
        'Particules fines - Agriculture': 'disease inc./kg',
        'Effets toxicologiques sur la santé humaine : substances non-cancérogènes': 'kg Sb eq/kg',
        'Effets toxicologiques sur la santé humaine : substances cancérogènes': 'kg Sb eq/kg',
        'Acidification terrestre et eaux douces': 'mol H+ eq/kg',
        'Eutrophisation eaux douces': 'kg P eq/kg',
        'Eutrophisation marine': 'kg N eq/kg',
        'Eutrophisation terrestre': 'mol N eq/kg',
        'Écotoxicité pour écosystèmes aquatiques d\'eau douce': 'CTUe/kg',
        'Utilisation du sol': 'Pt/kg',
        'Épuisement des ressources eau': 'm3 depriv./kg',
        'Épuisement des ressources énergétiques': 'MJ/kg',
        'Épuisement des ressources minéraux': 'kg Sb eq/kg',
        'Changement climatique - émissions biogéniques': 'kg CO2 eq/kg',
        'Changement climatique - émissions fossiles': 'kg CO2 eq/kg',
        'Changement climatique - émissions liées au changement d\'affectation des sols': 'kg CO2 eq/kg'
    }

    indicateur_selectionne = st.radio("Choisissez un indicateur :", impacts)

    colonne_indicateur = None
    for col in df_agribalyse.columns:
        if indicateur_selectionne in col and etape_selectionnee in col:
            colonne_indicateur = col
            break

    if not colonne_indicateur:
        st.warning("Colonne introuvable pour cette combinaison.")
        return

    df_panier[colonne_indicateur] = pd.to_numeric(df_panier[colonne_indicateur], errors='coerce')
    moyenne_panier = df_panier[colonne_indicateur].mean()

    sous_groupes = df_panier["Sous-groupe d'aliment"]
    moyennes = df_agribalyse.groupby("Sous-groupe d'aliment")[colonne_indicateur].mean()

    total_pondere = 0
    total_n = 0

    for sous_groupe in sous_groupes:
        if sous_groupe in moyennes.index:
            total_pondere += moyennes[sous_groupe]
            total_n += 1

    moyenne_sous_groupes = total_pondere / total_n if total_n > 0 else 0

    st.write(f"🔹 **Moyenne du panier** : {moyenne_panier:.4f} {unites[indicateur_selectionne]}")
    st.write(f"🔹 **Moyenne pondérée par sous-groupe** : {moyenne_sous_groupes:.4f} {unites[indicateur_selectionne]}")

    # === NOUVEAU : Diagramme en étoile pour l'indicateur sélectionné ===
    st.subheader(f"Comparaison par étape – {indicateur_selectionne}")

    valeurs_panier_indic = {}
    moyennes_sous_groupes_indic = {}

    for etape in etapes:
        colonne_cible = None
        for col in df_agribalyse.columns:
            if indicateur_selectionne in col and etape in col:
                colonne_cible = col
                break

        if not colonne_cible:
            continue

        df_panier[colonne_cible] = pd.to_numeric(df_panier[colonne_cible], errors='coerce')
        df_agribalyse[colonne_cible] = pd.to_numeric(df_agribalyse[colonne_cible], errors='coerce')

        # Moyenne directe du panier
        valeurs_panier_indic[etape] = df_panier[colonne_cible].mean()

        # Moyenne pondérée par sous-groupes
        moyennes = df_agribalyse.groupby("Sous-groupe d'aliment")[colonne_cible].mean()
        total, count = 0, 0

        for sg in sous_groupes:
            if sg in moyennes.index:
                total += moyennes[sg]
                count += 1

        moyennes_sous_groupes_indic[etape] = total / count if count > 0 else 0

    fig_indic_radar = go.Figure()

    fig_indic_radar.add_trace(go.Scatterpolar(
        r=list(valeurs_panier_indic.values()),
        theta=list(valeurs_panier_indic.keys()),
        fill='toself',
        name="Panier (moyenne directe)"
    ))

    fig_indic_radar.add_trace(go.Scatterpolar(
        r=list(moyennes_sous_groupes_indic.values()),
        theta=list(moyennes_sous_groupes_indic.keys()),
        fill='toself',
        name="Panier (moyenne sous-groupes)"
    ))

    fig_indic_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True,
        title=f"{indicateur_selectionne} par étape"
    )

    st.plotly_chart(fig_indic_radar)
