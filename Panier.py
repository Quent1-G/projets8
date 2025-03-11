# Ajout d'un produit
if "ajouter_produit" not in st.session_state:
    st.session_state.ajouter_produit = True

if st.session_state.ajouter_produit:
    search_query = st.text_input("Recherchez un produit par nom")

    if search_query:
        produits_trouves = df_ingredients[df_ingredients["Nom Français"].str.contains(search_query, case=False, na=False)]
        
        if not produits_trouves.empty:
            produit_selectionne = st.selectbox("Sélectionnez un produit", produits_trouves["Nom Français"].unique())

            code_ciqual = produits_trouves[produits_trouves["Nom Français"] == produit_selectionne]["Ciqual  code"].values[0]
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
