import streamlit as st
import pandas as pd
import plotly.express as px

# Fonction principale pour gérer et afficher les variables environnementales
def variables():
    # Charger la base de données
    df_synthese = pd.read_csv("agribalyse-31-synthese.csv", delimiter=',', dtype=str)

    # Initialiser le panier (si ce n'est pas déjà fait)
    if "panier" not in st.session_state:
        st.session_state.panier = []

    # Fonction pour calculer les indicateurs environnementaux du panier
    def calculer_indicateurs_panier():
        if not st.session_state.panier:
            return None, None, None

        # Récupérer les codes CIQUAL des produits dans le panier
        codes_ciqual = [item["code_ciqual"] for item in st.session_state.panier]

        # Filtrer les produits correspondant aux codes CIQUAL du panier
        produits_synthese = df_synthese[df_synthese["Code CIQUAL"].astype(str).isin(map(str, codes_ciqual))]

        if produits_synthese.empty:
            return None, None, None

        # Sélectionner les colonnes d'impact environnemental
        colonnes_impact = [
            'Changement climatique', 'Appauvrissement de la couche d\'ozone', 'Rayonnements ionisants', 
            'Formation photochimique d\'ozone', 'Particules fines', 
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
        
        produits_synthese[colonnes_impact] = produits_synthese[colonnes_impact].astype(float)

        # Calcul de la somme des impacts pour chaque variable
        total_impacts = produits_synthese[colonnes_impact].sum()
        total_somme = total_impacts.sum()  # Somme totale de toutes les variables

        return total_somme, total_impacts, produits_synthese

    # Interface Streamlit pour afficher les informations
    st.title("📊 Suivi des Indicateurs Environnementaux du Panier")

    # Sélectionner une variable environnementale à afficher
    selected_variable = st.selectbox(
        "🔍 Choisissez une variable environnementale à afficher",
        ['Changement climatique', 'Appauvrissement de la couche d\'ozone', 'Rayonnements ionisants', 
         'Formation photochimique d\'ozone', 'Particules fines', 
         'Effets toxicologiques sur la santé humaine : substances non-cancérogènes',
         'Effets toxicologiques sur la santé humaine : substances cancérogènes', 
         'Acidification terrestre et eaux douces', 'Eutrophisation eaux douces', 
         'Eutrophisation marine', 'Eutrophisation terrestre', 
         'Écotoxicité pour écosystèmes aquatiques d\'eau douce', 'Utilisation du sol', 
         'Épuisement des ressources eau', 'Épuisement des ressources énergétiques', 
         'Épuisement des ressources minéraux', 'Changement climatique - émissions biogéniques',
         'Changement climatique - émissions fossiles', 
         'Changement climatique - émissions liées au changement d\'affectation des sols']
    )

    # Calcul des indicateurs environnementaux pour le panier
    indicateurs_totaux, details_produits, produits_synthese = calculer_indicateurs_panier()

    # Vérification si les indicateurs sont disponibles
    if indicateurs_totaux is not None:
        st.subheader("📊 Indicateur environnemental du panier")

        # Calcul de la somme des valeurs pour la variable sélectionnée
        somme_variable = indicateurs_totaux[selected_variable]

        # Affichage de la somme des valeurs pour la variable sélectionnée
        st.metric(label=f"Somme des {selected_variable}", value=f"{somme_variable:.2f}")

        # Calcul de la contribution des produits sur la variable sélectionnée
        contribution = produits_synthese[selected_variable] / somme_variable * 100
        contribution = contribution.sort_values(ascending=False)

        # Affichage du graphique montrant la contribution en pourcentage de chaque produit
        noms_produits = [item["nom"] for item in st.session_state.panier]
        fig = px.bar(
            x=noms_produits,
            y=contribution.values,
            labels={'x': 'Produit', 'y': f'Contribution en % de {selected_variable}'},
            title=f"Contribution des produits pour {selected_variable}"
        )
        st.plotly_chart(fig)
    else:
        st.warning("Votre panier est vide. Ajoutez des produits pour voir les indicateurs environnementaux.")

