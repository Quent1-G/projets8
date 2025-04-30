import streamlit as st
import pandas as pd
import plotly.express as px

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

    # Étapes et impacts disponibles
    etapes = ["Agriculture", "Transformation", "Emballage", "Transport", "Supermarché et distribution", "Consommation"]
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

    # Sélection de l'étape
    etape_selectionnee = st.selectbox("Sélectionnez une étape à afficher :", etapes)

    # Sélection de l'indicateur environnemental
    impact_selectionne = st.selectbox("Sélectionnez un indicateur d’impact environnemental :", impacts)

    # Filtrer la colonne correspondant à l'étape + impact sélectionnés
    colonnes_match = [col for col in df_agribalyse.columns if etape_selectionnee in col and impact_selectionne in col]

    if not colonnes_match:
        st.error(f"Aucune colonne trouvée pour l'étape '{etape_selectionnee}' et l'impact '{impact_selectionne}'.")
        return

    colonne = colonnes_match[0]  # suppose une seule correspondance

    # Convertir la colonne en numérique
    df_panier[colonne] = pd.to_numeric(df_panier[colonne], errors="coerce")

    # Somme des valeurs du panier pour l'étape + impact sélectionnés
    somme_valeurs_panier = df_panier[colonne].sum()

    # Récupération des sous-groupes des produits du panier
    sous_groupes_panier = df_panier["Sous-groupe d'aliment"]

    # Moyennes des sous-groupes pour la colonne concernée
    moyennes_sous_groupes = df_agribalyse.groupby("Sous-groupe d'aliment")[colonne].mean()

    # Moyenne pondérée en tenant compte des répétitions des sous-groupes
    occurrences_sous_groupes = sous_groupes_panier.value_counts()
    somme_ponderee = sum(moyennes_sous_groupes.get(sg, 0) * count for sg, count in occurrences_sous_groupes.items())
    moyenne_ponderee_sous_groupes = somme_ponderee / occurrences_sous_groupes.sum()

    # Affichage des résultats
    unite = unites.get(impact_selectionne, "unité inconnue")

    st.subheader(f"Analyse pour l'étape : {etape_selectionnee}")
    st.write(f"🔹 **Somme des valeurs du panier** : {somme_valeurs_panier:.4f} {unite}")
    st.write(f"🔹 **Moyenne pondérée des sous-groupes** : {moyenne_ponderee_sous_groupes:.4f} {unite}")

    # Comparaison sous forme d'histogramme
    data_plot = pd.DataFrame({
        "Catégorie": ["Somme des valeurs du panier", "Moyenne pondérée des sous-groupes"],
        "Valeur": [somme_valeurs_panier, moyenne_ponderee_sous_groupes]
    })

    fig = px.bar(data_plot, x="Catégorie", y="Valeur", title=f"{impact_selectionne} - {etape_selectionnee}", color="Catégorie")
    st.plotly_chart(fig)
