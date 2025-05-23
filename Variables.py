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
        st.warning("Ajoutez des produits pour voir les indicateurs environnementaux.")
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

    # Vérifier si la variable environnementale existe
    if selected_variable not in produits_synthese.columns:
        st.warning(f"La variable environnementale {selected_variable} n'existe pas dans la base de données.")
        return

    # Convertir les valeurs de la colonne sélectionnée en float
    produits_synthese[selected_variable] = pd.to_numeric(produits_synthese[selected_variable], errors='coerce')

    # Vérifier la présence de données valides
    if produits_synthese[selected_variable].isnull().all():
        st.warning(f"Aucune valeur valide trouvée pour {selected_variable}.")
        return

    # Calcul de la somme des valeurs pour la variable sélectionnée
    somme_variable = produits_synthese[selected_variable].sum()

    # Afficher la somme des valeurs pour la variable environnementale sélectionnée avec l'unité
    if somme_variable > 0:
        st.metric(label=f"Somme des {selected_variable}", value=f"{somme_variable:.10f} {unites_variables[selected_variable]}")
    else:
        st.warning(f"Le résultat des {selected_variable} est inférieur ou égal à 0. Cela peut être dû à des données manquantes ou incorrectes.")
        return

    # Si somme valide, calculer la contribution de chaque produit
    produits_synthese['Contribution (%)'] = (produits_synthese[selected_variable] / somme_variable) * 100

    # Associer proprement les noms et contributions
    correspondance = []
    for item in st.session_state.panier:
        code = str(item['code_ciqual'])
        nom = item['nom']
        ligne = produits_synthese[produits_synthese["Code CIQUAL"].astype(str) == code]
        if not ligne.empty:
            contribution = ligne['Contribution (%)'].values[0]
            correspondance.append({'Produit': nom, 'Contribution (%)': contribution})

    # Créer un DataFrame propre
    df_graph = pd.DataFrame(correspondance)

    # Trier les produits par contribution décroissante
    df_graph = df_graph.sort_values(by='Contribution (%)', ascending=False)

    # Créer le graphique
    fig = px.bar(
        df_graph,
        x='Produit',
        y='Contribution (%)',
        labels={'Produit': 'Produit', 'Contribution (%)': f'Contribution (%) de {selected_variable}'},
        title=f"Contribution des produits pour {selected_variable}",
        text='Contribution (%)'
    )

    # Mise en forme du graphique
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig.update_layout(xaxis_title='Produit', yaxis_title='Contribution (%)', yaxis_tickformat='.2f')

    # Afficher le graphique
    st.plotly_chart(fig)

