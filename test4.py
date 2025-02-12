import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="Analyse des Produits Agro-Alimentaires",
    page_icon="🌱",
    layout="wide"
)

# Chargement des bases de données
df = pd.read_csv("agribalyse-31-detail-par-etape.csv", delimiter=',', dtype=str)
df_ingredients = pd.read_csv("Agribalyse_Detail ingredient.csv", delimiter=',', dtype=str)  # Remplace par le bon chemin

# Nettoyage des noms de colonnes
df.columns = df.columns.str.strip()
df_ingredients.columns = df_ingredients.columns.str.strip()

# Fonction pour filtrer les produits
def filtrer_produit(code_ciqual, etape):
    produit_filtre = df[df['Code CIQUAL'].astype(str) == str(code_ciqual)]
    if produit_filtre.empty:
        return "Aucun produit trouvé pour ce Code CIQUAL."
    
    colonnes_etape = [col for col in df.columns if etape in col]
    if not colonnes_etape:
        return f"Aucune donnée disponible pour l'étape '{etape}'."
    
    infos = produit_filtre[colonnes_etape].T.dropna()
    return infos

# Fonction pour filtrer les ingrédients
def filtrer_ingredients(code_ciqual, ingredient_selectionne):
    produit_ingredients = df_ingredients[df_ingredients['Ciqual  code'].astype(str) == str(code_ciqual)]
    if produit_ingredients.empty:
        return "Aucun ingrédient trouvé pour ce Code CIQUAL."
    
    colonnes_impact = df_ingredients.columns[6:24]
    
    if ingredient_selectionne:
        produit_ingredients = produit_ingredients[produit_ingredients['Ingredients'] == ingredient_selectionne]
    
    if produit_ingredients.empty:
        return f"Aucun résultat pour l'ingrédient '{ingredient_selectionne}'."
    
    impact_values = produit_ingredients[colonnes_impact].T
    impact_values.columns = [ingredient_selectionne]
    impact_values.insert(0, "Impact environnemental", impact_values.index)
    return impact_values.reset_index(drop=True)

# Style personnalisé
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 50px;
            font-weight: bold;
            color: #2E8B57;
        }
        .result-box {
            padding: 15px;
            border-radius: 10px;
            background-color: #F0F8FF;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Interface Streamlit
st.markdown('<p class="title">📊 Analyse des Produits Agro-Alimentaires</p>', unsafe_allow_html=True)

# Zone de recherche
search_query = st.text_input("🔍 Recherchez un produit par nom (ex: 'pomme', 'riz', etc.)")

if search_query:
    produits_trouves = df_ingredients[df_ingredients["Nom Français"].str.contains(search_query, case=False, na=False)]
    
    if not produits_trouves.empty:
        produit_selectionne = st.selectbox("🎯 Sélectionnez un produit", produits_trouves["Nom Français"].unique())
        code_ciqual = produits_trouves[produits_trouves["Nom Français"] == produit_selectionne]["Ciqual  code"].values[0]
        
        st.success(f"✔️ Produit sélectionné : {produit_selectionne} (Code CIQUAL : {code_ciqual})")
        
        # Sélection d'une étape
        etapes = ["Agriculture", "Transformation", "Emballage", "Transport", "Supermarché et distribution", "Consommation"]
        etape_selectionnee = st.radio("🛠️ Choisissez une étape du cycle de vie", etapes)
        
        # Affichage des résultats
        st.subheader("📌 Données du produit")
        result = filtrer_produit(code_ciqual, etape_selectionnee)
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.write(result)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sélection des ingrédients
        ingredients_dispo = df_ingredients[df_ingredients['Ciqual  code'].astype(str) == str(code_ciqual)]['Ingredients'].dropna().unique().tolist()
        
        if ingredients_dispo:
            st.subheader("🌿 Sélection des ingrédients")
            ingredient_selectionne = st.radio("🔬 Choisissez un ingrédient", ingredients_dispo)
            
            st.subheader("🌍 Impacts environnementaux de l'ingrédient sélectionné")
            result_ing = filtrer_ingredients(code_ciqual, ingredient_selectionne)
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.write(result_ing)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Aucun ingrédient disponible pour ce produit.")
    else:
        st.warning("🚫 Aucun produit ne correspond à votre recherche.")
