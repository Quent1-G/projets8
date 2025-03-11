import streamlit as st
import pandas as pd
import plotly.express as px

# Fonction principale pour gérer et afficher les variables environnementales
def variables():
    # Charger la base de données
    df_synthese = pd.read_csv("agribalyse-31-synthese.csv", delimiter=',', dtype=str)

 
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
