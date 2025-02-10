import streamlit as st
import pandas as pd

# Charger la base de données
df = pd.read_csv("agribalyse-31-detail-par-etape.csv", delimiter=';', dtype=str)
print(df.head(5))
def filtrer_produit(code_ciqual, etape):
    # Vérifier le type et filtrer correctement
    produit_filtre = df[df['Code CIQUAL'].astype(str) == str(code_ciqual)]
    
    if produit_filtre.empty:
        return "Aucun produit trouvé pour ce Code CIQUAL."

    # Filtrer les colonnes correspondant à l'étape choisie
    colonnes_etape = [col for col in df.columns if etape in col]
    
    if not colonnes_etape:
        return f"Aucune donnée disponible pour l'étape '{etape}'."

    infos = produit_filtre[colonnes_etape].T.dropna()
    return infos

# Interface Streamlit
st.title("Analyse des produits agro-alimentaires")

code_ciqual = st.text_input("Entrez un Code CIQUAL")

etapes = ["Agriculture", "Transformation", "Emballage", "Transport", "Supermarché et distribution", "Consommation"]
etape_selectionnee = st.radio("Choisissez une étape du cycle de vie", etapes)

if st.button("Afficher les résultats"):
    result = filtrer_produit(code_ciqual, etape_selectionnee)
    st.write(result)
