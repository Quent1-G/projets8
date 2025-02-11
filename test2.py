import streamlit as st
import pandas as pd

# Charger les bases de données
df = pd.read_csv("agribalyse-31-detail-par-etape.csv", delimiter=',', dtype=str)
df_ingredients = pd.read_csv("Agribalyse_Details ingredient.csv", delimiter=',', dtype=str)  # Remplace par le bon chemin

# Normaliser les noms de colonnes pour éviter les erreurs d'espace ou casse
df.columns = df.columns.str.strip()
df_ingredients.columns = df_ingredients.columns.str.strip()

def filtrer_produit(code_ciqual, etape):
    produit_filtre = df[df['Code CIQUAL'].astype(str) == str(code_ciqual)]
    if produit_filtre.empty:
        return "Aucun produit trouvé pour ce Code CIQUAL."

    colonnes_etape = [col for col in df.columns if etape in col]
    if not colonnes_etape:
        return f"Aucune donnée disponible pour l'étape '{etape}'."

    infos = produit_filtre[colonnes_etape].T.dropna()
    return infos

def filtrer_ingredients(code_ciqual):
    produit_ingredients = df_ingredients[df_ingredients['Ciqual  code'].astype(str) == str(code_ciqual)]
    if produit_ingredients.empty:
        return "Aucun ingrédient trouvé pour ce Code CIQUAL."
    
    # Colonnes index 1 et de 6 à 23
    colonnes_affichage = list(df_ingredients.columns[[1]] ) + list(df_ingredients.columns[6:24])
    return produit_ingredients[colonnes_affichage]

# Interface Streamlit
st.title("Analyse des produits agro-alimentaires")

# Interface utilisateur
code_ciqual = st.text_input("Entrez un Code CIQUAL")

# Liste des étapes et des ingrédients
etapes = ["Agriculture", "Transformation", "Emballage", "Transport", "Supermarché et distribution", "Consommation"]
etape_selectionnee = st.radio("Choisissez une étape du cycle de vie", etapes)

# Récupérer les ingrédients disponibles
ingredients_disponibles = df_ingredients['Ingredients'].dropna().unique().tolist()
ingredients_selectionnes = st.multiselect("Sélectionnez des ingrédients", ingredients_disponibles)

if st.button("Afficher les résultats"):
    col1, col2 = st.columns(2)  # Deux colonnes pour l'affichage

    with col1:
        st.subheader("Données du produit")
        result = filtrer_produit(code_ciqual, etape_selectionnee)
        st.write(result)

    with col2:
        st.subheader("Ingrédients")
        result_ing = filtrer_ingredients(code_ciqual)
        st.write(result_ing)
