import streamlit as st
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import plotly.express as px
import uuid
import datetime

# Set page configuration
st.set_page_config(page_title="Évaluation Carbone des Projets", layout="wide")

# Initialize session state for project history
if 'project_history' not in st.session_state:
    st.session_state['project_history'] = []

# Function to calculate carbon score (simplified model)
def calculate_carbon_score(energy, transport, materials, project_duration, team_size):
    # Base scores for different features
    energy_scores = {'Renouvelable': 10, 'Mix': 50, 'Fossile': 90}
    transport_scores = {'Local': 20, 'Régional': 40, 'International': 80}
    material_scores = {'Recyclé': 15, 'Bois': 30, 'Béton': 70}
    
    # Weighted scoring
    score = (
        0.4 * energy_scores.get(energy, 50) +
        0.3 * transport_scores.get(transport, 50) +
        0.2 * material_scores.get(materials, 50) +
        0.05 * (project_duration / 12) * 10 +  # Duration in months
        0.05 * (team_size / 50) * 10  # Team size normalized
    )
    
    # Ensure score is between 0 and 100
    return min(max(round(score, 2), 0), 100)

# Function to classify project using decision tree
def classify_project(data):
    # Simulated training data for decision tree
    X_train = pd.DataFrame({
        'energy': ['Renouvelable', 'Fossile', 'Mix', 'Renouvelable', 'Fossile'],
        'transport': ['Local', 'International', 'Régional', 'Local', 'International'],
        'materials': ['Recyclé', 'Béton', 'Bois', 'Recyclé', 'Béton'],
        'score': [20, 90, 50, 25, 85]
    })
    y_train = ['Vert', 'Très polluant', 'Acceptable', 'Vert', 'Très polluant']
    
    # Encode categorical variables
    le = LabelEncoder()
    X_train_encoded = X_train[['energy', 'transport', 'materials']].apply(le.fit_transform)
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train_encoded, y_train)
    
    # Prepare input data
    input_data = pd.DataFrame({
        'energy': [data['energy']],
        'transport': [data['transport']],
        'materials': [data['materials']]
    })
    input_encoded = input_data.apply(le.fit_transform)
    
    # Predict classification
    return clf.predict(input_encoded)[0]

# Function to generate recommendations based on association rules (simplified)
def generate_recommendations(energy, transport, materials):
    recommendations = []
    if energy == 'Fossile':
        recommendations.append("Passer à une énergie renouvelable (solaire, éolien) pour réduire l'empreinte carbone.")
    if transport == 'International':
        recommendations.append("Privilégier des fournisseurs locaux ou régionaux pour minimiser les émissions de transport.")
    if materials == 'Béton':
        recommendations.append("Utiliser des matériaux recyclés ou du bois certifié pour une construction plus durable.")
    if not recommendations:
        recommendations.append("Projet déjà optimisé. Continuez à privilégier des pratiques durables.")
    return recommendations

# Main Streamlit app
st.title("Évaluation de l'Empreinte Carbone des Projets")

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Choisir une page", ["Soumettre un Projet", "Historique des Projets", "Comparaison des Projets"])

if page == "Soumettre un Projet":
    st.header("Formulaire de Soumission de Projet")
    
    with st.form(key='project_form'):
        project_name = st.text_input("Nom du Projet")
        sector = st.selectbox("Secteur", ["Construction", "Transport", "Industrie", "Agriculture", "Numérique"])
        energy = st.selectbox("Type d'Énergie", ["Renouvelable", "Mix", "Fossile"])
        transport = st.selectbox("Type de Transport", ["Local", "Régional", "International"])
        materials = st.selectbox("Matériaux Principaux", ["Recyclé", "Bois", "Béton"])
        project_duration = st.slider("Durée du Projet (mois)", 1, 120, 12)
        team_size = st.slider("Taille de l'Équipe", 1, 500, 50)
        uploaded_file = st.file_uploader("Description du Projet (PDF/Texte)", type=['pdf', 'txt'])
        submit_button = st.form_submit_button("Évaluer le Projet")
        
        if submit_button:
            if project_name:
                # Calculate carbon score
                carbon_score = calculate_carbon_score(energy, transport, materials, project_duration, team_size)
                
                # Classify project
                project_data = {'energy': energy, 'transport': transport, 'materials': materials}
                classification = classify_project(project_data)
                
                # Generate recommendations
                recommendations = generate_recommendations(energy, transport, materials)
                
                # Save project to history
                project_id = str(uuid.uuid4())
                project_record = {
                    'ID': project_id,
                    'Nom': project_name,
                    'Secteur': sector,
                    'Score Carbone': carbon_score,
                    'Classification': classification,
                    'Date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state['project_history'].append(project_record)
                
                # Display results
                st.subheader("Résultats de l'Évaluation")
                st.write(f"**Score Carbone :** {carbon_score}/100")
                st.write(f"**Classification :** {classification}")
                
                # Visualize contributing factors
                factors = pd.DataFrame({
                    'Facteur': ['Énergie', 'Transport', 'Matériaux', 'Durée', 'Équipe'],
                    'Impact': [
                        0.4 * {'Renouvelable': 10, 'Mix': 50, 'Fossile': 90}.get(energy, 50),
                        0.3 * {'Local': 20, 'Régional': 40, 'International': 80}.get(transport, 50),
                        0.2 * {'Recyclé': 15, 'Bois': 30, 'Béton': 70}.get(materials, 50),
                        0.05 * (project_duration / 12) * 10,
                        0.05 * (team_size / 50) * 10
                    ]
                })
                fig = px.bar(factors, x='Facteur', y='Impact', title="Impact des Facteurs sur le Score Carbone")
                st.plotly_chart(fig)
                
                # Display recommendations
                st.subheader("Recommandations")
                for rec in recommendations:
                    st.write(f"- {rec}")
                
                # Download report button
                st.download_button(
                    label="Télécharger le Rapport",
                    data=f"""
                    Rapport d'Évaluation Carbone
                    Nom du Projet: {project_name}
                    Secteur: {sector}
                    Score Carbone: {carbon_score}/100
                    Classification: {classification}
                    Recommandations:
                    {chr(10).join(['- ' + r for r in recommendations])}
                    """.encode(),
                    file_name=f"rapport_{project_name}.txt",
                    mime="text/plain"
                )
            else:
                st.error("Veuillez entrer un nom de projet.")

elif page == "Historique des Projets":
    st.header("Historique des Projets")
    if st.session_state['project_history']:
        history_df = pd.DataFrame(st.session_state['project_history'])
        st.dataframe(history_df)
    else:
        st.info("Aucun projet soumis pour le moment.")

elif page == "Comparaison des Projets":
    st.header("Comparaison des Projets")
    if st.session_state['project_history']:
        history_df = pd.DataFrame(st.session_state['project_history'])
        fig = px.bar(history_df, x='Nom', y='Score Carbone', color='Classification',
                     title="Comparaison des Scores Carbone des Projets")
        st.plotly_chart(fig)
    else:
        st.info("Aucun projet soumis pour le moment.")