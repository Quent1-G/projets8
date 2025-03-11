import streamlit as st
import pandas as pd
import plotly.express as px

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

    # Afficher la somme des valeurs pour la variable environnementale sélectionnée
    st.metric(label=f"Somme des {selected_variable}", value=f"{somme_variable:.2f}")
