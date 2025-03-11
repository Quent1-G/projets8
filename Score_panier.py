import streamlit as st
import pandas as pd

# Charger la base de données
df_synthese_finale = pd.read_csv("Synthese_finale.csv")

def score_panier():
       #ici je veux faire la moyenne des scores de mon panier pour les afficher ensuite sur une jauge
