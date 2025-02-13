import streamlit as st
import pandas as pd
import plotly.express as px

# Charger les bases de données
df = pd.read_csv("agribalyse-31-detail-par-etape.csv", delimiter=',', dtype=str)
df_ingredients = pd.read_csv("Agribalyse_Detail ingredient.csv", delimiter=',', dtype=str)  # Remplace par le bon chemin
df_synthese = pd.read_csv("agribalyse-31-synthese.csv", delimiter=',', dtype=str)  # Nouvelle BDD

# Normaliser les noms de colonnes
df.columns = df.columns.str.strip()
df_ingredients.columns = df_ingredients.columns.str.strip()
df_synthese.columns = df_synthese.columns.str.strip()

# Initialiser le panier dans la session si non existant
if "panier" not in st.session_state:
    st.session_state.panier = []

# Fonction pour filtrer les produits selon le code CIQUAL
def filtrer_produit(code_ciqual, etape):
    produit_filtre = df[df['Code CIQUAL'].astype(str) == str(code_ciqual)]
    if produit_filtre.empty:
        return "Aucun produit trouvé pour ce Code CIQUAL."

    colonnes_etape = [col for col in df.columns if etape in col]
    if not colonnes_etape:
        return f"Aucune donnée disponible pour l'étape '{etape}'."

    return produit_filtre[colonnes_etape].T.dropna()

# Fonction pour récupérer les indicateurs environnementaux du panier
def calculer_indicateurs_panier():
    if not st.session_state.panier:
        return None
    
    # Extraire les codes CIQUAL du panier
    codes_ciqual = [item["code_ciqual"] for item in st.session_state.panier]
    
    # Filtrer la BDD Synthèse pour ces produits
    produits_synthese = df_synthese[df_synthese["Code CIQUAL"].astype(str).isin(map(str, codes_ciqual))]
    
    if produits_synthese.empty:
        return None

    # Sélection des colonnes d'index 12 à 31
    colonnes_impact = produits_synthese.columns[12:32]
    
    # Convertir les valeurs en float et sommer
    produits_synthese[colonnes_impact] = produits_synthese[colonnes_impact].astype(float)
    total_impacts = produits_synthese.groupby("Code CIQUAL")[colonnes_impact].sum()
    total_somme = total_impacts.sum()

    return total_somme, total_impacts

# Interface Streamlit
st.title("Analyse des produits agro-alimentaires")

# Zone de recherche par mot-clé
search_query = st.text_input("Recherchez un produit par nom (ex: 'pomme', 'riz', etc.)")

if search_query:
    produits_trouves = df_ingredients[df_ingredients["Nom Français"].str.contains(search_query, case=False, na=False)]
    
    if not produits_trouves.empty:
        produit_selectionne = st.selectbox("Sélectionnez un produit", produits_trouves["Nom Français"].unique())

        # Récupérer le code CIQUAL correspondant
        code_ciqual = produits_trouves[produits_trouves["Nom Français"] == produit_selectionne]["Ciqual  code"].values[0]

        st.success(f"Produit sélectionné : {produit_selectionne} (Code CIQUAL : {code_ciqual})")

        # Ajouter au panier
        if st.button("Ajouter au panier"):
            st.session_state.panier.append({"nom": produit_selectionne, "code_ciqual": code_ciqual})
            st.success(f"{produit_selectionne} ajouté au panier.")

# Affichage du panier
st.subheader("📦 Votre panier")
if st.session_state.panier:
    for index, item in enumerate(st.session_state.panier):
        col1, col2 = st.columns([4, 1])
        col1.write(f"🔹 {item['nom']} (Code CIQUAL: {item['code_ciqual']})")
        if col2.button("❌", key=f"remove_{index}"):
            del st.session_state.panier[index]
            st.rerun()

    # Vérifier si le panier contient des produits avant de calculer les indicateurs
    if st.session_state.panier:
        indicateurs_totaux, details_produits = calculer_indicateurs_panier()
        st.subheader("📊 Indicateurs environnementaux du panier")
        st.write(indicateurs_totaux)  # Affiche le tableau des indicateurs
    
else:
    st.info("Votre panier est vide.")


# Calcul des indicateurs du panier
indicateurs_totaux, details_produits = calculer_indicateurs_panier()

if indicateurs_totaux is not None:
    st.subheader("📊 Impact environnemental du panier")
    
    # Affichage du tableau des indicateurs
    df_indicateurs = pd.DataFrame({"Impact environnemental": indicateurs_totaux.index, "Valeur totale": indicateurs_totaux.values})
    selected_indicator = st.dataframe(df_indicateurs.set_index("Impact environnemental"))

    # Graphique interactif sur la contribution des produits
    selected_row = st.selectbox("Sélectionnez un indicateur pour voir la contribution des aliments", df_indicateurs["Impact environnemental"])

    if selected_row:
        contribution = details_produits[selected_row]
        contribution = contribution / contribution.sum() * 100  # Calcul du pourcentage
        contribution = contribution.sort_values(ascending=False)

        fig = px.bar(contribution, x=contribution.index, y=contribution.values, labels={'x': 'Produit', 'y': 'Contribution (%)'}, title=f"Contribution des produits pour {selected_row}")
        st.plotly_chart(fig)

# Sélection d'un produit dans le panier pour voir ses détails
if st.session_state.panier:
    st.subheader("🔍 Explorer un produit du panier")
    produit_choisi = st.selectbox("Sélectionnez un produit", [item["nom"] for item in st.session_state.panier])

    if produit_choisi:
        code_ciqual_choisi = next(item["code_ciqual"] for item in st.session_state.panier if item["nom"] == produit_choisi)
        
        # Liste des étapes du cycle de vie
        etapes = ["Agriculture", "Transformation", "Emballage", "Transport", "Supermarché et distribution", "Consommation"]
        etape_selectionnee = st.radio("Choisissez une étape du cycle de vie", etapes, key="etape_produit")

        st.subheader("Données du produit")
        result = filtrer_produit(code_ciqual_choisi, etape_selectionnee)
        st.write(result)

        # Récupérer les ingrédients disponibles
        ingredients_dispo = df_ingredients[df_ingredients['Ciqual  code'].astype(str) == str(code_ciqual_choisi)]['Ingredients'].dropna().unique().tolist()

        if ingredients_dispo:
            st.subheader("Sélection des ingrédients")
            ingredient_selectionne = st.radio("Choisissez un ingrédient", ingredients_dispo, key="ingredient_produit")

            # Affichage du tableau des impacts environnementaux
            st.subheader("Impacts environnementaux de l'ingrédient sélectionné")
            result_ing = filtrer_produit(code_ciqual_choisi, ingredient_selectionne)
            st.write(result_ing)
        else:
            st.warning("Aucun ingrédient disponible pour ce produit.")
