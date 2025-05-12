import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np  # Pour la normalisation

@st.cache_data
def charger_bdd():
    return pd.read_csv("agribalyse-31-detail-par-etape.csv")

def graphique_radar(df_agribalyse, df_panier, sous_groupes_panier, variable_selectionnee):
    st.subheader("Comparaison radar des étapes - Variable sélectionnée")

    etapes = [
        "Agriculture", "Transformation", "Emballage", "Transport",
        "Supermarché et distribution", "Consommation"
    ]

    valeurs_panier = []
    valeurs_panier_moyenne = []

    for etape in etapes:
        colonnes_etape = [col for col in df_agribalyse.columns if etape in col and variable_selectionnee in col]

        if colonnes_etape:
            # Valeurs panier utilisateur
            somme_etape_utilisateur = df_panier[colonnes_etape].sum().sum()
            valeurs_panier.append(somme_etape_utilisateur)

            # Valeurs panier moyen similaire
            moyennes_sous_groupes = df_agribalyse.groupby("Sous-groupe d'aliment")[colonnes_etape].mean()
            moyenne_etape = sum(
                moyennes_sous_groupes.loc[sous_groupe].sum()
                for sous_groupe in sous_groupes_panier
                if sous_groupe in moyennes_sous_groupes.index
            )
            valeurs_panier_moyenne.append(moyenne_etape)
        else:
            valeurs_panier.append(0)
            valeurs_panier_moyenne.append(0)

    # 🔽 Centrage-réduction par colonne
    valeurs_panier_cr = []
    valeurs_panier_moyenne_cr = []

    for v, v_moyenne in zip(valeurs_panier, valeurs_panier_moyenne):
        # Calcul de la moyenne et de l'écart type de chaque colonne (étape)
        moyenne = np.mean([v, v_moyenne])
        ecart_type = np.std([v, v_moyenne]) if np.std([v, v_moyenne]) != 0 else 1

        # Application du centrage-réduction
        valeurs_panier_cr.append((v - moyenne) / ecart_type)
        valeurs_panier_moyenne_cr.append((v_moyenne - moyenne) / ecart_type)

    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=valeurs_panier_cr,
        theta=etapes,
        fill='toself',
        name='Panier utilisateur'
    ))

    fig_radar.add_trace(go.Scatterpolar(
        r=valeurs_panier_moyenne_cr,
        theta=etapes,
        fill='toself',
        name='Panier moyen similaire'
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True)
        ),
        showlegend=True,
        title=f"Radar - {variable_selectionnee} (centré-réduit)"
    )

    st.plotly_chart(fig_radar)

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
    etape_selectionnee = st.selectbox("Sélectionnez une étape à afficher :", etapes)

    colonnes_etape = [col for col in df_agribalyse.columns if etape_selectionnee in col]

    if not colonnes_etape:
        st.error(f"Aucune colonne trouvée pour l'étape '{etape_selectionnee}'.")
        return

    df_panier[colonnes_etape] = df_panier[colonnes_etape].apply(pd.to_numeric, errors="coerce")

    somme_valeurs_panier = df_panier[colonnes_etape].sum().sum()
    sous_groupes_panier = df_panier["Sous-groupe d'aliment"]
    moyennes_sous_groupes = df_agribalyse.groupby("Sous-groupe d'aliment")[colonnes_etape].mean()

    somme_moyennes_sous_groupes = sum(
        moyennes_sous_groupes.loc[sous_groupe].sum()
        for sous_groupe in sous_groupes_panier
        if sous_groupe in moyennes_sous_groupes.index
    )

    st.subheader(f"Analyse pour l'étape : {etape_selectionnee}")
    st.write(f"🔹 **Somme des valeurs du panier** : {somme_valeurs_panier:.2f}")
    st.write(f"🔹 **Somme des moyennes des sous-groupes** : {somme_moyennes_sous_groupes:.2f}")

    data_plot = pd.DataFrame({
        "Catégorie": ["Somme des valeurs du panier", "Somme des moyennes des sous-groupes"],
        "Valeur": [somme_valeurs_panier, somme_moyennes_sous_groupes]
    })

    fig = px.bar(data_plot, x="Catégorie", y="Valeur", title=f"Comparaison pour {etape_selectionnee}", color="Catégorie")
    st.plotly_chart(fig)

    # ---------------------------------------
    # 🔽 Analyse détaillée par indicateur
    # ---------------------------------------

    impacts = [
        "Score unique EF", "Changement climatique", "Appauvrissement de la couche d'ozone",
        "Rayonnements ionisants", "Formation photochimique d'ozone", "Particules fines - Agriculture",
        "Effets toxicologiques sur la santé humaine : substances non-cancérogènes",
        "Effets toxicologiques sur la santé humaine : substances cancérogènes",
        "Acidification terrestre et eaux douces", "Eutrophisation eaux douces",
        "Eutrophisation marine", "Eutrophisation terrestre",
        "Écotoxicité pour écosystèmes aquatiques d'eau douce", "Utilisation du sol",
        "Épuisement des ressources eau", "Épuisement des ressources énergétiques",
        "Épuisement des ressources minéraux", "Changement climatique - émissions biogéniques",
        "Changement climatique - émissions fossiles",
        "Changement climatique - émissions liées au changement d'affectation des sols"
    ]

    unites = {
        'Score unique EF': 'sans unité',
        'Changement climatique': 'kg CO2 eq/kg',
        "Appauvrissement de la couche d'ozone": 'kg CVC11 eq/kg',
        "Rayonnements ionisants": 'kBq U-235 eq/kg',
        "Formation photochimique d'ozone": 'kg NMVOC eq/kg',
        "Particules fines - Agriculture": 'disease inc./kg',
        "Effets toxicologiques sur la santé humaine : substances non-cancérogènes": 'kg Sb eq/kg',
        "Effets toxicologiques sur la santé humaine : substances cancérogènes": 'kg Sb eq/kg',
        "Acidification terrestre et eaux douces": 'mol H+ eq/kg',
        "Eutrophisation eaux douces": 'kg P eq/kg',
        "Eutrophisation marine": 'kg N eq/kg',
        "Eutrophisation terrestre": 'mol N eq/kg',
        "Écotoxicité pour écosystèmes aquatiques d'eau douce": 'CTUe/kg',
        "Utilisation du sol": 'Pt/kg',
        "Épuisement des ressources eau": 'm3 depriv./kg',
        "Épuisement des ressources énergétiques": 'MJ/kg',
        "Épuisement des ressources minéraux": 'kg Sb eq/kg',
        "Changement climatique - émissions biogéniques": 'kg CO2 eq/kg',
        "Changement climatique - émissions fossiles": 'kg CO2 eq/kg',
        "Changement climatique - émissions liées au changement d'affectation des sols": 'kg CO2 eq/kg',
    }

    st.subheader("Analyse détaillée par indicateur")

    impact_selectionne = st.selectbox("Sélectionnez un indicateur d’impact environnemental :", impacts)

    colonnes_match = [col for col in df_agribalyse.columns if etape_selectionnee in col and impact_selectionne in col]
    if not colonnes_match:
        st.error(f"Aucune donnée disponible pour l'étape '{etape_selectionnee}' et l'indicateur '{impact_selectionne}'.")
        return

    colonne = colonnes_match[0]
    df_panier[colonne] = pd.to_numeric(df_panier[colonne], errors="coerce")

    moyenne_panier = df_panier[colonne].mean()
    moyennes_sous_groupes = df_agribalyse.groupby("Sous-groupe d'aliment")[colonne].mean()
    occurrences_sous_groupes = sous_groupes_panier.value_counts()

    somme_ponderee = sum(
        moyennes_sous_groupes.get(sg, 0) * count
        for sg, count in occurrences_sous_groupes.items()
    )
    moyenne_ponderee = somme_ponderee / occurrences_sous_groupes.sum()

    unite = unites.get(impact_selectionne, "unité inconnue")

    st.write(f"🔹 **Moyenne du panier pour** *{impact_selectionne}* : {moyenne_panier:.4f} {unite}")
    st.write(f"🔹 **Moyenne pondérée des sous-groupes** : {moyenne_ponderee:.4f} {unite}")

    data_plot2 = pd.DataFrame({
        "Catégorie": ["Moyenne du panier", "Moyenne pondérée des sous-groupes"],
        "Valeur": [moyenne_panier, moyenne_ponderee]
    })

    fig2 = px.bar(data_plot2, x="Catégorie", y="Valeur", title=f"{impact_selectionne} - {etape_selectionnee}", color="Catégorie")
    st.plotly_chart(fig2)


