import streamlit as st
import pandas as pd
import plotly.express as px

# Chargement de la BDD (Assure-toi que le chemin du fichier est correct)
@st.cache_data
def charger_bdd():
    return pd.read_csv("agribalyse-31-detail-par-etape.csv")

def etapes_panier():
    st.header("Analyse des étapes du panier")

    # Récupérer les codes CIQUAL du panier depuis la session
    if "panier" not in st.session_state or not st.session_state.panier:
        st.warning("Le panier est vide. Ajoutez des produits pour voir l'analyse.")
        return

    codes_ciqual_panier = [int(produit["code_ciqual"]) for produit in st.session_state.panier]

    # Charger la BDD étapes
    df_agribalyse = charger_bdd()

    # Vérifier que la colonne "Code CIQUAL" existe
    if "Code CIQUAL" not in df_agribalyse.columns:
        st.error("Erreur : La colonne 'Code CIQUAL' est introuvable dans la BDD.")
        return

    # Filtrer la BDD pour ne garder que les produits du panier
    df_panier = df_agribalyse[df_agribalyse["Code CIQUAL"].isin(codes_ciqual_panier)]

    # Vérifier si des produits du panier existent dans la BDD
    if df_panier.empty:
        st.warning("Aucun des produits du panier ne correspond à la BDD étapes.")
        return

    # Sélection de l'étape
    etapes = ["Agriculture", "Transformation", "Emballage", "Transport", "Supermarché et distribution", "Consommation"]
    etape_selectionnee = st.selectbox("Sélectionnez une étape à afficher :", etapes)

    # Filtrer les colonnes contenant l'étape sélectionnée
    colonnes_etape = [col for col in df_agribalyse.columns if etape_selectionnee in col]

    if not colonnes_etape:
        st.error(f"Aucune colonne trouvée pour l'étape '{etape_selectionnee}'.")
        return

    # Assurer que les colonnes sont numériques
    df_panier[colonnes_etape] = df_panier[colonnes_etape].apply(pd.to_numeric, errors="coerce")

    # Calcul de la somme des valeurs des individus du panier pour l'étape sélectionnée
    somme_valeurs_panier = df_panier[colonnes_etape].sum().sum()

    # Calcul de la moyenne des valeurs des "Sous-groupe d'aliment"
    moyennes_sous_groupes = df_agribalyse.groupby("Sous-groupe d'aliment")[colonnes_etape].mean()

    # Moyenne des moyennes pour les sous-groupes des produits du panier
    moyennes_panier = moyennes_sous_groupes.loc[df_panier["Sous-groupe d'aliment"]].mean().sum()

    # Affichage des résultats
    st.subheader(f"Analyse pour l'étape : {etape_selectionnee}")
    st.write(f"🔹 **Somme des valeurs du panier** : {somme_valeurs_panier:.2f}")
    st.write(f"🔹 **Moyenne des sous-groupes d'aliment** : {moyennes_panier:.2f}")

    # Comparaison sous forme d'histogramme
    data_plot = pd.DataFrame({
        "Catégorie": ["Somme des valeurs du panier", "Moyenne des sous-groupes d'aliment"],
        "Valeur": [somme_valeurs_panier, moyennes_panier]
    })

    fig = px.bar(data_plot, x="Catégorie", y="Valeur", title=f"Comparaison pour {etape_selectionnee}", color="Catégorie")
    st.plotly_chart(fig)

