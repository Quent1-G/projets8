import streamlit as st
import pandas as pd
import plotly.express as px

# Charger les bases de données
df = pd.read_csv("agribalyse-31-detail-par-etape.csv", delimiter=',', dtype=str)
df_ingredients = pd.read_csv("Agribalyse_Detail ingredient.csv", delimiter=',', dtype=str)
df_synthese = pd.read_csv("agribalyse-31-synthese.csv", delimiter=',', dtype=str)

# Normaliser les noms de colonnes
df.columns = df.columns.str.strip()
df_ingredients.columns = df_ingredients.columns.str.strip()
df_synthese.columns = df_synthese.columns.str.strip()

# Dictionnaire des unités par indicateur
unites_indicateurs = {
    "Changement climatique": "kg CO2 eq",
    "Particules fines": "disease incidence",
    "Épuisement des ressources en eau": "m3 world eq",
    "Épuisement des ressources énergétiques": "MJ",
    "Usage des terres": "point",
    "Épuisement des ressources - minéraux": "kg Sb eq",
    "Appauvrissement de la couche d’ozone": "kg CFC-11 eq",
    "Acidification": "mol H+ eq",
    "Radiation ionisante, effet sur la santé": "kBq U235 eq",
    "Formation photochimique d’ozone": "kg NMVOC eq",
    "Eutrophisation, terrestre": "mol N eq",
    "Eutrophisation, marine": "kg N eq",
    "Eutrophisation, eau douce": "kg P eq",
    "Ecotoxicité d'eau douce": "CTUe",
    "Effets toxicologiques sur la santé humaine - non-cancérogènes": "CTUh",
    "Effets toxicologiques sur la santé humaine - cancérogènes": "CTUh",
}

# Initialiser le panier
if "panier" not in st.session_state:
    st.session_state.panier = []

# Fonction pour calculer les indicateurs du panier
def calculer_indicateurs_panier():
    if not st.session_state.panier:
        return None, None

    codes_ciqual = [item["code_ciqual"] for item in st.session_state.panier]
    produits_synthese = df_synthese[df_synthese["Code CIQUAL"].astype(str).isin(map(str, codes_ciqual))]

    if produits_synthese.empty:
        return None, None

    colonnes_impact = produits_synthese.columns[12:32]
    
    # Sécuriser la conversion en float
    produits_synthese[colonnes_impact] = produits_synthese[colonnes_impact].apply(pd.to_numeric, errors="coerce").fillna(0)

    total_impacts = produits_synthese.groupby("Code CIQUAL")[colonnes_impact].sum()
    total_somme = total_impacts.sum()

    return total_somme, total_impacts

# Interface Streamlit
st.title("Analyse des produits agro-alimentaires")

# Ajout d'un produit
if "ajouter_produit" not in st.session_state:
    st.session_state.ajouter_produit = True

if st.session_state.ajouter_produit:
    search_query = st.text_input("Recherchez un produit par nom")

    if search_query:
        produits_trouves = df_ingredients[df_ingredients["Nom Français"].str.contains(search_query, case=False, na=False)]
        
        if not produits_trouves.empty:
            produit_selectionne = st.selectbox("Sélectionnez un produit", produits_trouves["Nom Français"].unique())

            code_ciqual = produits_trouves.loc[produits_trouves["Nom Français"] == produit_selectionne, "Ciqual  code"].values[0]
            st.success(f"Produit sélectionné : {produit_selectionne} (Code CIQUAL : {code_ciqual})")

            if st.button("Ajouter au panier"):
                st.session_state.panier.append({"nom": produit_selectionne, "code_ciqual": code_ciqual})
                st.session_state.ajouter_produit = False
                st.rerun()

if st.button("Ajouter un autre produit"):
    st.session_state.ajouter_produit = True
    st.rerun()

# Affichage du panier
st.subheader("📦 Votre panier")
if st.session_state.panier:
    for index, item in enumerate(st.session_state.panier):
        col1, col2 = st.columns([4, 1])
        col1.write(f"🔹 {item['nom']}")
        if col2.button("❌", key=f"remove_{index}"):
            del st.session_state.panier[index]
            st.rerun()
else:
    st.info("Votre panier est vide.")

# Calcul et affichage des indicateurs environnementaux du panier
indicateurs_totaux, details_produits = calculer_indicateurs_panier()

if indicateurs_totaux is not None:
    st.subheader("📊 Indicateurs environnementaux du panier")

    df_indicateurs = pd.DataFrame({
        "Impact environnemental": indicateurs_totaux.index,
        "Valeur totale": indicateurs_totaux.values,
        "Unité": [unites_indicateurs.get(indicateur, "N/A") for indicateur in indicateurs_totaux.index]
    })

    st.dataframe(df_indicateurs.set_index("Impact environnemental"))

# Exploration des ingrédients
st.subheader("🧑‍🍳 Ingrédients du produit sélectionné")

if st.session_state.panier:
    produit_choisi = st.selectbox("Sélectionnez un produit", [item["nom"] for item in st.session_state.panier])

    if produit_choisi:
        code_ciqual_choisi = next(item["code_ciqual"] for item in st.session_state.panier if item["nom"] == produit_choisi)

        ingredients_dispo = df_ingredients[df_ingredients['Ciqual  code'].astype(str) == str(code_ciqual_choisi)]['Ingredients'].dropna().unique().tolist()

        if ingredients_dispo:
            ingredient_selectionne = st.radio("Choisissez un ingrédient", ingredients_dispo, key="ingredient_produit")

            impact_ingredient = df_ingredients[
                (df_ingredients['Ciqual  code'].astype(str) == str(code_ciqual_choisi)) & 
                (df_ingredients['Ingredients'] == ingredient_selectionne)
            ]

            if not impact_ingredient.empty:
                colonnes_impact = impact_ingredient.columns[6:24]
                
                # Sécurisation de la conversion
                impact_values = impact_ingredient[colonnes_impact].apply(pd.to_numeric, errors="coerce").fillna(0).T
                impact_values.columns = [ingredient_selectionne]

                impact_values.insert(0, "Impact environnemental", impact_values.index)
                impact_values["Unité"] = [unites_indicateurs.get(indic, "N/A") for indic in impact_values["Impact environnemental"]]

                st.dataframe(impact_values.set_index("Impact environnemental"))

                fig = px.bar(
                    x=impact_values.index,
                    y=impact_values[ingredient_selectionne],
                    labels={'x': 'Indicateur environnemental', 'y': 'Valeur'},
                    title=f"Impacts environnementaux de {ingredient_selectionne}",
                    color=impact_values[ingredient_selectionne],
                    color_continuous_scale="RdYlGn_r"
                )
                st.plotly_chart(fig)
            else:
                st.warning(f"Aucun impact trouvé pour '{ingredient_selectionne}'.")
        else:
            st.warning("Aucun ingrédient disponible pour ce produit.")
