import streamlit as st

# Titre de l'application
st.title("Test Hello World")

# Afficher un message
st.write("Hello, World! Bienvenue dans l'environnement virtuel.")

# Ajouter un bouton interactif
if st.button("Cliquez ici"):
    st.balloons()
    st.write("Vous avez cliqué sur le bouton ! Le test est réussi.")