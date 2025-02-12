import streamlit as st
import pandas as pd

# Charger les bases de données
df = pd.read_csv("agribalyse-31-detail-par-etape.csv", delimiter=',', dtype=str)
df_ingredients = pd.read_csv("Agribalyse_Detail ingredient.csv", delimiter=',', dtype=str)

# Normaliser les noms de colonnes pour éviter les erreurs d'espace ou casse
df.columns = df.columns.str.strip()
df_ingredients.columns = df_ingredients.columns.str.strip()

# Fonction pour filtrer les produits selon le code CIQUAL
def filtrer_produit(code_ciqual, etape):
    produit_filtre = df[df['Code CIQUAL'].astype(str) == str(code_ciqual)]
    if produit_filtre.empty:
        return "Aucun produit trouvé pour ce Code CIQUAL."

    colonnes_etape = [col for col in df.columns if etape in col]
    if not colonnes_etape:
        return f"Aucune donnée disponible pour l'étape '{etape}'."

    infos = produit_filtre[colonnes_etape].T.dropna()
    return infos

# Fonction pour filtrer les ingrédients selon le Code CIQUAL
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


# Ajouter du CSS personnalisé
st.markdown(
    """
    <style>
    /* Style pour le contenu principal */
    .main-content {
        margin-right: 250px;  /* Espace pour le bandeau latéral à droite */
        padding: 20px;
        overflow-y: scroll;
        height: 100vh;  /* Remplir l'écran */
    }

    /* Style du bandeau latéral à droite */
    .sidebar {
        position: fixed;
        top: 0;
        right: 0;  /* Fixer le bandeau à droite */
        width: 250px;  /* Largeur du bandeau */
        height: 100vh;  /* Hauteur maximale pour occuper toute la hauteur */
        background-color: #83ca69;  /* Couleur de fond du bandeau */
        overflow-y: auto;  /* Permet au bandeau d'être défilable */
        padding: 20px;
        box-shadow: -2px 0px 5px rgba(0, 0, 0, 0.1);  /* Ombre à gauche pour séparation */
        z-index: 10;
    }

    /* Style du contenu du bandeau latéral */
    .sidebar .stSidebar > div {
        padding: 20px;
        font-size: 18px;
    }

    </style>
    """, unsafe_allow_html=True
)

# Interface principale
st.markdown('<div class="main-content">', unsafe_allow_html=True)

################################################################################################## page principale
# Interface Streamlit
st.title("Analyse des produits agro-alimentaires")

# Zone de recherche par mot-clé
search_query = st.text_input("Recherchez un produit par nom (ex: 'pomme', 'riz', etc.)")

# Liste des produits correspondant au mot-clé
if search_query:
    produits_trouves = df_ingredients[df_ingredients["Nom Français"].str.contains(search_query, case=False, na=False)]
    
    if not produits_trouves.empty:
        produit_selectionne = st.selectbox("Sélectionnez un produit", produits_trouves["Nom Français"].unique())

        code_ciqual = produits_trouves[produits_trouves["Nom Français"] == produit_selectionne]["Ciqual  code"].values[0]

        st.success(f"Produit sélectionné : {produit_selectionne} (Code CIQUAL : {code_ciqual})")

        etapes = ["Agriculture", "Transformation", "Emballage", "Transport", "Supermarché et distribution", "Consommation"]
        etape_selectionnee = st.radio("Choisissez une étape du cycle de vie", etapes)

        st.subheader("Données du produit")
        result = filtrer_produit(code_ciqual, etape_selectionnee)
        st.write(result)

        ingredients_dispo = df_ingredients[df_ingredients['Ciqual  code'].astype(str) == str(code_ciqual)]['Ingredients'].dropna().unique().tolist()

        if ingredients_dispo:
            st.subheader("Sélection des ingrédients")
            ingredient_selectionne = st.radio("Choisissez un ingrédient", ingredients_dispo)

            st.subheader("Impacts environnementaux de l'ingrédient sélectionné")
            result_ing = filtrer_ingredients(code_ciqual, ingredient_selectionne)
            st.write(result_ing)
        else:
            st.warning("Aucun ingrédient disponible pour ce produit.")
    else:
        st.warning("Aucun produit ne correspond à votre recherche.")

################################################################################################ page secondaire
# Interface du bandeau latéral (à droite)
st.sidebar.markdown('<div class="sidebar">', unsafe_allow_html=True)

# Contenu du bandeau latéral
st.sidebar.title("Options de Menu")
st.sidebar.radio("Choisissez une option", ["Option 1", "Option 2", "Option 3"])
st.sidebar.write("Plus de détails ici...")

st.sidebar.markdown('</div>', unsafe_allow_html=True)
