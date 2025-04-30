import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def charger_bdd():
    return pd.read_csv("agribalyse-31-detail-par-etape.csv")

def graphique_radar(df_agribalyse, df_panier, variable_selectionnee, sous_groupes_panier):
    # Définir les étapes (axes du radar)
    etapes = ["Agriculture", "Transformation", "Emballage", "Transport", "Supermarché et distribution", "Consommation"]
    
    # Initialiser les listes pour les valeurs du panier et du panier moyen
    valeurs_panier = []
    valeurs_panier_moyenne = []
    
    # Calcul des sommes pour chaque étape pour le panier de l'utilisateur
    for etape in etapes:
        colonnes_etape = [col for col in df_agribalyse.columns if etape in col and variable_selectionnee in col]
        if colonnes_etape:
            somme_etape = df_panier[colonnes_etape].sum().sum()
            valeurs_panier.append(somme_etape)
        else:
            valeurs_panier.append(0)

    # Calcul du panier moyen similaire
    moyennes_sous_groupes = df_agribalyse.groupby("Sous-groupe d'aliment")[colonnes_etape].mean()
    somme_moyennes_sous_groupes = 0

    for etape in etapes:
        colonnes_etape = [col for col in df_agribalyse.columns if etape in col and variable_selectionnee in col]
        moyenne_etape = sum(moyennes_sous_groupes.loc[sous_groupe].sum() for sous_groupe in sous_groupes_panier)
        valeurs_panier_moyenne.append(moyenne_etape)
    
    # Créer le graphique radar
    fig = go.Figure()

    # Ajouter les données du panier de l'utilisateur
    fig.add_trace(go.Scatterpolar(
        r=valeurs_panier,
        theta=etapes,
        fill='toself',
        name='Panier Utilisateur'
    ))

    # Ajouter les données du panier moyen similaire
    fig.add_trace(go.Scatterpolar(
        r=valeurs_panier_moyenne,
        theta=etapes,
        fill='toself',
        name='Panier Moyen Similaire'
    ))

    # Mise en forme du graphique
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(max(valeurs_panier), max(valeurs_panier_moyenne))])
        ),
        showlegend=True,
        title=f"Comparaison Radar : {variable_selectionnee}"
    )

    st.plotly_chart(fig)

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

    # Sélection de la variable à comparer (impact environnemental)
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
    
    variable_selectionnee = st.selectbox("Sélectionnez une variable d'impact environnemental :", impacts)

    # Récupérer les sous-groupes du panier utilisateur
    sous_groupes_panier = df_panier["Sous-groupe d'aliment"]

    # Afficher le graphique radar
    graphique_radar(df_agribalyse, df_panier, variable_selectionnee, sous_groupes_panier)

    # ---------------------------------
    # Graphique 1 : Comparaison des valeurs du panier et des moyennes des sous-groupes
    # ---------------------------------
    etapes = ["Agriculture", "Transformation", "Emballage", "Transport", "Supermarché et distribution", "Consommation"]
    
    colonnes_etape = [col for col in df_agribalyse.columns if variable_selectionnee in col]
    
    # Somme des valeurs du panier pour la variable sélectionnée
    somme_valeurs_panier = df_panier[colonnes_etape].sum().sum()

    # Moyennes des sous-groupes pour la variable sélectionnée
    moyennes_sous_groupes = df_agribalyse.groupby("Sous-groupe d'aliment")[colonnes_etape].mean()

    # Calcul de la somme des moyennes en tenant compte des répétitions
    somme_moyennes_sous_groupes = sum(moyennes_sous_groupes.loc[sous_groupe].sum() for sous_groupe in sous_groupes_panier)

    # Affichage des résultats
    st.subheader(f"Analyse pour la variable : {variable_selectionnee}")
    st.write(f"🔹 **Somme des valeurs du panier** : {somme_valeurs_panier:.2f}")
    st.write(f"🔹 **Somme des moyennes des sous-groupes** : {somme_moyennes_sous_groupes:.2f}")

    # Comparaison sous forme d'histogramme
    data_plot = pd.DataFrame({
        "Catégorie": ["Somme des valeurs du panier", "Somme des moyennes des sous-groupes"],
        "Valeur": [somme_valeurs_panier, somme_moyennes_sous_groupes]
    })

    fig = px.bar(data_plot, x="Catégorie", y="Valeur", title=f"Comparaison pour {variable_selectionnee}", color="Catégorie")
    st.plotly_chart(fig)

    # ---------------------------------
    # Graphique 2 : Indicateur spécifique
    # ---------------------------------

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

    # Trouver la colonne correspondant à la variable sélectionnée
    colonnes_match = [col for col in df_agribalyse.columns if impact_selectionne in col]
    if not colonnes_match:
        st.error(f"Aucune donnée disponible pour l'indicateur '{impact_selectionne}'.")
        return

    colonne = colonnes_match[0]

    # Convertir la colonne en numérique
    df_panier[colonne] = pd.to_numeric(df_panier[colonne], errors="coerce")

    # Moyenne brute du panier pour cet indicateur
    moyenne_panier = df_panier[colonne].mean()

    # Moyenne pondérée des sous-groupes
    moyennes_sous_groupes = df_agribalyse.groupby("Sous-groupe d'aliment")[colonne].mean()
    occurrences_sous_groupes = sous_groupes_panier.value_counts()
    somme_ponderee = sum(moyennes_sous_groupes.get(sg, 0) * count for sg, count in occurrences_sous_groupes.items())
    moyenne_ponderee = somme_ponderee / occurrences_sous_groupes.sum()

    # Affichage
    unite = unites.get(impact_selectionne, "unité inconnue")

    st.write(f"🔹 **Moyenne du panier pour** *{impact_selectionne}* : {moyenne_panier:.4f} {unite}")
    st.write(f"🔹 **Moyenne pondérée des sous-groupes** : {moyenne_ponderee:.4f} {unite}")

    # Deuxième graphique
    data_plot2 = pd.DataFrame({
        "Catégorie": ["Moyenne du panier", "Moyenne pondérée des sous-groupes"],
        "Valeur": [moyenne_panier, moyenne_ponderee]
    })

    fig2 = px.bar(data_plot2, x="Catégorie", y="Valeur", title=f"{impact_selectionne}", color="Catégorie")
    st.plotly_chart(fig2)
