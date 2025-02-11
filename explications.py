# Importation des bibliothèques nécessaires
import streamlit as st  # Streamlit pour créer une interface utilisateur interactive
import pandas as pd     # Pandas pour manipuler les données tabulaires

# Charger les bases de données depuis des fichiers CSV
df = pd.read_csv("agribalyse-31-detail-par-etape.csv", delimiter=',', dtype=str)  
# Lecture du fichier CSV contenant les détails des produits agroalimentaires
# `dtype=str` force tous les champs à être lus comme des chaînes de caractères

df_ingredients = pd.read_csv("Agribalyse_Detail ingredient.csv", delimiter=',', dtype=str)  
# Lecture du fichier CSV contenant les informations sur les ingrédients
# Remplacer "Agribalyse_Detail ingredient.csv" par le chemin correct du fichier

# Normaliser les noms de colonnes pour éviter les erreurs dues aux espaces ou aux différences de casse
df.columns = df.columns.str.strip()  
df_ingredients.columns = df_ingredients.columns.str.strip()  

# ================================
# Fonction pour filtrer les données d'un produit selon le Code CIQUAL et l'étape sélectionnée
# ================================
def filtrer_produit(code_ciqual, etape):
    # Filtrer le DataFrame `df` pour ne garder que les lignes correspondant au Code CIQUAL fourni
    produit_filtre = df[df['Code CIQUAL'].astype(str) == str(code_ciqual)]
    
    # Vérifier si le produit a été trouvé
    if produit_filtre.empty:
        return "Aucun produit trouvé pour ce Code CIQUAL."

    # Sélectionner les colonnes correspondant à l'étape choisie (ex: "Agriculture", "Transformation", etc.)
    colonnes_etape = [col for col in df.columns if etape in col]

    # Vérifier si des données existent pour cette étape
    if not colonnes_etape:
        return f"Aucune donnée disponible pour l'étape '{etape}'."

    # Transposer les données sélectionnées pour un affichage plus clair et supprimer les valeurs vides
    infos = produit_filtre[colonnes_etape].T.dropna()
    return infos  # Retourne les données filtrées sous forme de tableau

# ================================
# Fonction pour filtrer les ingrédients selon le Code CIQUAL et afficher les impacts environnementaux
# ================================
def filtrer_ingredients(code_ciqual, ingredient_selectionne):
    # Filtrer le DataFrame `df_ingredients` pour ne garder que les lignes correspondant au Code CIQUAL fourni
    produit_ingredients = df_ingredients[df_ingredients['Ciqual  code'].astype(str) == str(code_ciqual)]
    
    # Vérifier si des ingrédients sont disponibles pour ce produit
    if produit_ingredients.empty:
        return "Aucun ingrédient trouvé pour ce Code CIQUAL."
    
    # Sélection des colonnes contenant les indicateurs environnementaux (index 6 à 23)
    colonnes_impact = df_ingredients.columns[6:24]
    
    if ingredient_selectionne:
        # Filtrer uniquement l'ingrédient sélectionné parmi les ingrédients du produit
        produit_ingredients = produit_ingredients[produit_ingredients['Ingredients'] == ingredient_selectionne]
    
    # Vérifier si un ingrédient correspondant a été trouvé
    if produit_ingredients.empty:
        return f"Aucun résultat pour l'ingrédient '{ingredient_selectionne}'."

    # Transposer les valeurs des indicateurs environnementaux pour un affichage structuré
    impact_values = produit_ingredients[colonnes_impact].T  # Les colonnes deviennent des lignes
    impact_values.columns = [ingredient_selectionne]  # Nommer la seule colonne avec le nom de l'ingrédient
    
    # Ajouter une colonne pour nommer chaque ligne "Impact environnemental"
    impact_values.insert(0, "Impact environnemental", impact_values.index)
    
    return impact_values.reset_index(drop=True)  # Réinitialiser les index pour un affichage propre

# ================================
# Interface utilisateur avec Streamlit
# ================================
st.title("Analyse des produits agro-alimentaires")  # Titre principal de l'application

# Zone de saisie du Code CIQUAL
code_ciqual = st.text_input("Entrez un Code CIQUAL")  # Zone de texte pour entrer un code

# Vérifier si un Code CIQUAL a été entré
if code_ciqual:
    # Liste des étapes du cycle de vie d'un produit agroalimentaire
    etapes = ["Agriculture", "Transformation", "Emballage", "Transport", "Supermarché et distribution", "Consommation"]
    
    # Création d'un bouton radio pour choisir une étape parmi la liste
    etape_selectionnee = st.radio("Choisissez une étape du cycle de vie", etapes)

    # Affichage des résultats pour le produit sélectionné
    st.subheader("Données du produit")  # Sous-titre
    result = filtrer_produit(code_ciqual, etape_selectionnee)  # Appel de la fonction de filtrage
    st.write(result)  # Affichage du tableau

    # Récupération des ingrédients liés au Code CIQUAL entré
    ingredients_dispo = df_ingredients[df_ingredients['Ciqual  code'].astype(str) == str(code_ciqual)]['Ingredients'].dropna().unique().tolist()

    # Vérifier si des ingrédients sont disponibles
    if ingredients_dispo:
        st.subheader("Sélection des ingrédients")  # Sous-titre
        ingredient_selectionne = st.radio("Choisissez un ingrédient", ingredients_dispo)  # Liste radio des ingrédients disponibles

        # Affichage des impacts environnementaux de l'ingrédient sélectionné
        st.subheader("Impacts environnementaux de l'ingrédient sélectionné")  # Sous-titre
        result_ing = filtrer_ingredients(code_ciqual, ingredient_selectionne)  # Appel de la fonction
        st.write(result_ing)  # Affichage du tableau

    else:
        # Message d'avertissement si aucun ingrédient n'est disponible pour ce produit
        st.warning("Aucun ingrédient disponible pour ce produit.")

else:
    # Message d'information demandant à l'utilisateur d'entrer un Code CIQUAL
    st.info("Veuillez entrer un Code CIQUAL pour voir les données.")
