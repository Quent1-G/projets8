import streamlit as st
import pandas as pd
import plotly.express as px

# Charger la base de données Agribalyse
df_agribalyse = pd.read_csv("agribalyse-31-detail-par-etape.csv")

def etapes_panier():
    """
    Calcule et affiche :
    - La somme des valeurs des produits du panier pour chaque variable environnementale
    - La somme des moyennes des catégories des produits du panier
    - Un histogramme comparant les deux valeurs
    """
    
    # Vérifier si le panier contient des produits
    if "panier" not in st.session_state or not st.session_state.panier:
        st.warning("Votre panier est vide.")
        return

    # Extraire les codes CIQUAL des produits du panier
    codes_ciqual_panier = [int(produit["code_ciqual"]) for produit in st.session_state.panier]

    # Filtrer la base Agribalyse pour ne garder que les produits du panier
    df_panier = df_agribalyse[df_agribalyse["Code CIQUAL"].isin(codes_ciqual_panier)]


    if df_panier.empty:
        st.warning("Aucun produit du panier trouvé dans la base Agribalyse.")
        return

    # Liste des variables environnementales (exclure les colonnes non pertinentes)
    colonnes_var_env = [col for col in df_agribalyse.columns if col not in ["code_ciqual", "nom_produit", "categorie"]]

    # Calcul de la somme des valeurs du panier pour chaque variable
    somme_valeurs_panier = df_panier[colonnes_var_env].sum()

    # Calcul des moyennes des catégories et somme de ces moyennes
    moyennes_categories = df_agribalyse.groupby("categorie")[colonnes_var_env].mean()
    somme_moyennes_categories = moyennes_categories.loc[df_panier["categorie"].unique()].sum()

    # Création du DataFrame pour affichage
    df_comparaison = pd.DataFrame({
        "Variable Environnementale": colonnes_var_env,
        "Valeur du Panier": somme_valeurs_panier.values,
        "Moyenne des Catégories": somme_moyennes_categories.values
    })

    # Affichage des valeurs sous forme de tableau
    st.subheader("📊 Comparaison des impacts environnementaux")
    st.write("Ci-dessous, une comparaison entre la somme des valeurs du panier et la somme des moyennes des catégories :")
    st.dataframe(df_comparaison)

    # Création de l'histogramme
    fig = px.bar(df_comparaison, 
                 x="Variable Environnementale", 
                 y=["Valeur du Panier", "Moyenne des Catégories"],
                 barmode="group",
                 title="Comparaison des impacts environnementaux du panier",
                 labels={"value": "Valeur", "variable": "Type"},
                 height=600)

    # Affichage du graphique
    st.plotly_chart(fig)
