import streamlit as st
import pandas as pd
import plotly.express as px

# Dictionnaire des unités correspondantes à chaque variable environnementale
unites_variables = {
    'Changement climatique': 'kg CO2 eq/kg',
    'Appauvrissement de la couche d\'ozone': 'kg CVC11 eq/kg',
    'Rayonnements ionisants': 'kBq U-235 eq/kg',
    'Formation photochimique d\'ozone': 'kg NMVOC eq/kg',
    'Particules fines': 'disease inc./kg',
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

# Fonction principale pour gérer et afficher les variables environnementales
def variables():
    # Charger la base de données
    df_synthese = pd.read_csv("agribalyse-31-synthese.csv", delimiter=',', dtype=str)

    # Vérifier si le panier existe dans le session_state
    if "panier" not in st.session_state:
        st.session_state.panier = []

    # Vérifier si le panier est vide
    if not st.session_state.panier:
        st.warning("Votre panier est vide. Ajoutez des produits pour voir les indicateurs environnementaux.")
        return

    # Afficher le titre
    st.title("📊 Suivi des Indicateurs Environnementaux du Panier")

    # Sélectionner une variable environnementale à afficher
    selected_variable = st.selectbox(
        "🔍 Choisissez une variable environnementale à afficher",
        list(unites_variables.keys())
    )

    # Extraire les codes CIQUAL des produits dans le panier
    codes_ciqual = [item["code_ciqual"] for item in st.session_state.panier]
    
    # Filtrer les produits dans la BDD par les codes CIQUAL du panier
    produits_synthese = df_synthese[df_synthese["Code CIQUAL"].astype(str).isin(map(str, codes_ciqual))]

    # Vérifier si des produits ont été trouvés
    if produits_synthese.empty:
        st.warning("Aucun produit correspondant aux codes CIQUAL dans le panier.")
        return

    # Convertir les valeurs de la colonne sélectionnée en float pour éviter des erreurs de type
    produits_synthese[selected_variable] = produits_synthese[selected_variable].astype(float)

    # Calculer la somme des valeurs pour la variable sélectionnée dans le panier
    somme_variable = produits_synthese[selected_variable].sum()

    # Afficher la somme des valeurs pour la variable environnementale sélectionnée avec l'unité
    st.metric(label=f"Somme des {selected_variable}", value=f"{somme_variable:.2f} {unites_variables[selected_variable]}")

    # Calcul de la contribution de chaque produit à la somme totale
    produits_synthese['Contribution (%)'] = (produits_synthese[selected_variable] / somme_variable) * 100

    # Trier les produits par contribution décroissante
    produits_synthese = produits_synthese.sort_values(by='Contribution (%)', ascending=False)

    # Affichage graphique de la contribution de chaque produit
    noms_produits = [item["nom"] for item in st.session_state.panier]
    contribution = produits_synthese['Contribution (%)']

    fig = px.bar(
        x=noms_produits,
        y=contribution,
        labels={'x': 'Produit', 'y': f'Contribution (%) de {selected_variable}'},
        title=f"Contribution des produits pour {selected_variable}"
    )
    st.plotly_chart(fig)
