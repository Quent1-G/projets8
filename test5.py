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

# Initialiser le panier dans la session si non existant
if "panier" not in st.session_state:
    st.session_state.panier = []

# Fonction pour récupérer les indicateurs environnementaux du panier
def calculer_indicateurs_panier():
    if not st.session_state.panier:
        return None, None

    codes_ciqual = [item["code_ciqual"] for item in st.session_state.panier]
    produits_synthese = df_synthese[df_synthese["Code CIQUAL"].astype(str).isin(map(str, codes_ciqual))]
    
    if produits_synthese.empty:
        return None, None

    colonnes_impact = produits_synthese.columns[12:32]
    produits_synthese[colonnes_impact] = produits_synthese[colonnes_impact].astype(float)
    total_impacts = produits_synthese.groupby("Code CIQUAL")[colonnes_impact].sum()
    total_somme = total_impacts.sum()

    return total_somme, total_impacts

# Interface Streamlit
st.title("Analyse des produits agro-alimentaires")

# Recherche d'un produit
search_query = st.text_input("Recherchez un produit par nom (ex: 'pomme', 'riz', etc.)")

if search_query:
    produits_trouves = df_ingredients[df_ingredients["Nom Français"].str.contains(search_query, case=False, na=False)]
    
    if not produits_trouves.empty:
        produit_selectionne = st.selectbox("Sélectionnez un produit", produits_trouves["Nom Français"].unique())
        code_ciqual = produits_trouves[produits_trouves["Nom Français"] == produit_selectionne]["Ciqual  code"].values[0]

        st.success(f"Produit sélectionné : {produit_selectionne} (Code CIQUAL : {code_ciqual})")

        if st.button("Ajouter au panier"):
            st.session_state.panier.append({"nom": produit_selectionne, "code_ciqual": code_ciqual})
            st.rerun()

# Affichage du panier
st.subheader("📦 Votre panier")
if st.session_state.panier:
    for index, item in enumerate(st.session_state.panier):
        col1, col2 = st.columns([4, 1])
        col1.write(f"🔹 {item['nom']} (Code CIQUAL: {item['code_ciqual']})")
        if col2.button("❌", key=f"remove_{index}"):
            del st.session_state.panier[index]
            st.rerun()

    indicateurs_totaux, details_produits = calculer_indicateurs_panier()
    
    if indicateurs_totaux is not None:
        st.subheader("📊 Indicateurs environnementaux du panier")
        
        df_indicateurs = pd.DataFrame({"Impact environnemental": indicateurs_totaux.index, "Valeur totale": indicateurs_totaux.values})
        st.dataframe(df_indicateurs.set_index("Impact environnemental"))

        # Vérifier que l'utilisateur a sélectionné un indicateur
        if not df_indicateurs.empty:
            selected_row = st.selectbox("Sélectionnez un indicateur", df_indicateurs["Impact environnemental"])

            if selected_row and selected_row in details_produits.columns:
                contribution = details_produits[selected_row]
                contribution = (contribution / contribution.sum()) * 100
                contribution = contribution.sort_values(ascending=False)

                fig = px.bar(contribution, x=contribution.index, y=contribution.values, 
                             labels={'x': 'Produit', 'y': 'Contribution (%)'}, 
                             title=f"Contribution des produits pour {selected_row}")
                st.plotly_chart(fig)
    
else:
    st.info("Votre panier est vide.")
