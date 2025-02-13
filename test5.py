import plotly.express as px
import plotly.colors as colors

# Dictionnaire des unités des indicateurs
unites = {
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
    "Effets toxicologiques sur la santé humaine (non-cancérogènes)": "CTUh",
    "Effets toxicologiques sur la santé humaine (cancérogènes)": "CTUh"
}

if selected_row:
    contribution = details_produits[selected_row]
    contribution = contribution / contribution.sum() * 100
    contribution = contribution.sort_values(ascending=False)

    # Définir une échelle de couleurs du vert au rouge
    colorscale = colors.sequential.RdYlGn_r

    fig = px.bar(
        contribution, 
        x=contribution.index, 
        y=contribution.values, 
        labels={'x': 'Produit', 'y': f"Contribution (%) - {unites.get(selected_row, '')}"}, 
        title=f"Contribution des produits pour {selected_row}",
        color=contribution.values, 
        color_continuous_scale=colorscale
    )
    
    fig.update_layout(coloraxis_colorbar=dict(title="Contribution (%)"))
    st.plotly_chart(fig)
