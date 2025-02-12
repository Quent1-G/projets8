import streamlit as st

# Fonction principale pour l'application
def app():
    ########################################################### TITRE ###################################
    # Titre de la page principale
    st.title("Ce qu'on met dans nos assietes, quel impact sur la planète ?")
    #####################################################################################################
     # Contenu du bandeau latéral
    ################################################## CONTENU BANDEAU ###########################
    st.sidebar.title("Contenu")
    st.sidebar.radio("Navigation", ["Accueil", "Contexte", "Méthodologie","Analyse globale"])
    st.sidebar.write("A propos :")
    st.sidebar.write("nous étudiants et bla bla bla...")
    ########################################### CONTENU PAGE ######################################
    # Contenu principal de la page
    st.write("aujourd'hui, bla bla bla, la conso et la planete bla bal bla")
# Lancer l'application
if __name__ == "__main__":
    app()
