import streamlit as st
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import plotly.express as px
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import uuid
import datetime

# Set page configuration
st.set_page_config(page_title="Évaluation Carbone des Projets", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for enhanced visuals
st.markdown("""
<style>
    .main {background-color: #f4f7fa;}
    .stButton>button {background-color: #2e7d32; color: white; border-radius: 8px; padding: 10px 20px;}
    .stButton>button:hover {background-color: #1b5e20;}
    .card {background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 20px;}
    .success {color: #2e7d32; font-weight: bold;}
    .warning {color: #ff9800; font-weight: bold;}
    .error {color: #d32f2f; font-weight: bold;}
    .stProgress .st-bo {background-color: #2e7d32;}
</style>
""", unsafe_allow_html=True)

# Initialize session state for project history
if 'project_history' not in st.session_state:
    st.session_state['project_history'] = []

# Function to calculate carbon score
def calculate_carbon_score(energy, transport, materials, project_duration, team_size):
    energy_scores = {'Renouvelable': 10, 'Mix': 50, 'Fossile': 90}
    transport_scores = {'Local': 20, 'Régional': 40, 'International': 80}
    material_scores = {'Recyclé': 15, 'Bois': 30, 'Béton': 70}
    score = (
        0.4 * energy_scores.get(energy, 50) +
        0.3 * transport_scores.get(transport, 50) +
        0.2 * material_scores.get(materials, 50) +
        0.05 * (project_duration / 12) * 10 +
        0.05 * (team_size / 50) * 10
    )
    return min(max(round(score, 2), 0), 100)

# Function to classify project
def classify_project(data):
    X_train = pd.DataFrame({
        'energy': ['Renouvelable', 'Fossile', 'Mix', 'Renouvelable', 'Fossile'],
        'transport': ['Local', 'International', 'Régional', 'Local', 'International'],
        'materials': ['Recyclé', 'Béton', 'Bois', 'Recyclé', 'Béton'],
        'score': [20, 90, 50, 25, 85]
    })
    y_train = ['Vert', 'Très polluant', 'Acceptable', 'Vert', 'Très polluant']
    le = LabelEncoder()
    X_train_encoded = X_train[['energy', 'transport', 'materials']].apply(le.fit_transform)
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train_encoded, y_train)
    input_data = pd.DataFrame({
        'energy': [data['energy']],
        'transport': [data['transport']],
        'materials': [data['materials']]
    })
    input_encoded = input_data.apply(le.fit_transform)
    return clf.predict(input_encoded)[0]

# Function to generate recommendations
def generate_recommendations(energy, transport, materials):
    recommendations = []
    if energy == 'F士ile':
        recommendations.append("Passer à une énergie renouvelable (solaire, éolien) pour réduire l'empreinte carbone.")
    if transport == 'International':
        recommendations.append("Privilégier des fournisseurs locaux ou régionaux pour minimiser les émissions de transport.")
    if materials == 'Béton':
        recommendations.append("Utiliser des matériaux recyclés ou du bois certifié pour une construction plus durable.")
    if not recommendations:
        recommendations.append("Projet déjà optimisé. Continuez à privilégier des pratiques durables.")
    return recommendations

# Function to generate PDF report
def generate_pdf_report(project_name, sector, carbon_score, classification, recommendations):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Rapport d'Évaluation Carbone")
    c.drawString(100, 730, f"Nom du Projet: {project_name}")
    c.drawString(100, 710, f"Secteur: {sector}")
    c.drawString(100, 690, f"Score Carbone: {carbon_score}/100")
    c.drawString(100, 670, f"Classification: {classification}")
    c.drawString(100, 650, "Recommandations:")
    y = 630
    for rec in recommendations:
        c.drawString(120, y, f"- {rec}")
        y -= 20
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# Main app
st.title("🌍 Évaluation de l'Empreinte Carbone des Projets")
st.markdown("Une application pour évaluer et optimiser l'impact environnemental des projets.")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.selectbox("Choisir une page", ["Soumettre un Projet", "Historique des Projets", "Comparaison des Projets"], help="Naviguez entre les différentes sections de l'application.")
    st.markdown("---")
    st.markdown("**À propos**")
    st.markdown("Cette application aide les institutions financières à évaluer l'empreinte carbone des projets et à proposer des recommandations durables.")

if page == "Soumettre un Projet":
    st.header("📋 Soumettre un Projet")
    with st.form(key='project_form'):
        col1, col2 = st.columns(2)
        with col1:
            project_name = st.text_input("Nom du Projet", help="Entrez un nom unique pour votre projet.")
            sector = st.selectbox("Secteur", ["Construction", "Transport", "Industrie", "Agriculture", "Numérique"], help="Sélectionnez le secteur du projet.")
            energy = st.selectbox("Type d'Énergie", ["Renouvelable", "Mix", "Fossile"], help="Type d'énergie principal utilisé.")
        with col2:
            transport = st.selectbox("Type de Transport", ["Local", "Régional", "International"], help="Mode de transport principal.")
            materials = st.selectbox("Matériaux Principaux", ["Recyclé", "Bois", "Béton"], help="Matériaux dominants dans le projet.")
            project_duration = st.slider("Durée du Projet (mois)", 1, 120, 12, help="Durée estimée en mois.")
            team_size = st.slider("Taille de l'Équipe", 1, 500, 50, help="Nombre de personnes impliquées.")
        uploaded_file = st.file_uploader("Description du Projet (PDF/Texte)", type=['pdf', 'txt'], help="Optionnel : joignez un document descriptif.")
        submit_button = st.form_submit_button("Évaluer le Projet")

        if submit_button:
            if project_name:
                with st.spinner("Analyse en cours..."):
                    # Calculate carbon score
                    carbon_score = calculate_carbon_score(energy, transport, materials, project_duration, team_size)
                    project_data = {'energy': energy, 'transport': transport, 'materials': materials}
                    classification = classify_project(project_data)
                    recommendations = generate_recommendations(energy, transport, materials)

                    # Save to history
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

                    # Animation based on classification
                    if classification == "Vert":
                        st.balloons()
                    elif classification == "Très polluant":
                        st.snow()

                    # Display results
                    st.markdown("### Résultats de l'Évaluation")
                    col_score, col_class = st.columns(2)
                    with col_score:
                        st.markdown(f"**Score Carbone :** <span class={'success' if carbon_score < 40 else 'warning' if carbon_score < 70 else 'error'}>{carbon_score}/100</span>", unsafe_allow_html=True)
                        fig_gauge = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=carbon_score,
                            gauge={
                                'axis': {'range': [0, 100]},
                                'bar': {'color': "#2e7d32" if carbon_score < 40 else "#ff9800" if carbon_score < 70 else "#d32f2f"},
                                'steps': [
                                    {'range': [0, 40], 'color': "#e8f5e9"},
                                    {'range': [40, 70], 'color': "#fff3e0"},
                                    {'range': [70, 100], 'color': "#ffebee"}
                                ]
                            }
                        ))
                        fig_gauge.update_layout(title="Score Carbone")
                        st.plotly_chart(fig_gauge, use_container_width=True)
                    with col_class:
                        st.markdown(f"**Classification :** <span class={'success' if classification == 'Vert' else 'warning' if classification == 'Acceptable' else 'error'}>{classification}</span>", unsafe_allow_html=True)

                    # Visualize factors
                    st.markdown("### Facteurs Contributifs")
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
                    fig_bar = px.bar(factors, x='Facteur', y='Impact', title="Impact des Facteurs", color='Impact', color_continuous_scale='RdYlGn_r')
                    st.plotly_chart(fig_bar, use_container_width=True)

                    # Display recommendations
                    st.markdown("### Recommandations")
                    with st.container():
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        for rec in recommendations:
                            st.markdown(f"✅ {rec}")
                        st.markdown('</div>', unsafe_allow_html=True)

                    # Download PDF report
                    pdf_buffer = generate_pdf_report(project_name, sector, carbon_score, classification, recommendations)
                    st.download_button(
                        label="Télécharger le Rapport PDF",
                        data=pdf_buffer,
                        file_name=f"rapport_{project_name}.pdf",
                        mime="application/pdf"
                    )
            else:
                st.error("Veuillez entrer un nom de projet.")

elif page == "Historique des Projets":
    st.header("📜 Historique des Projets")
    if st.session_state['project_history']:
        history_df = pd.DataFrame(st.session_state['project_history'])
        sector_filter = st.multiselect("Filtrer par Secteur", options=history_df['Secteur'].unique(), default=history_df['Secteur'].unique())
        filtered_df = history_df[history_df['Secteur'].isin(sector_filter)]
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.info("Aucun projet soumis pour le moment.")

elif page == "Comparaison des Projets":
    st.header("📊 Comparaison des Projets")
    if st.session_state['project_history']:
        history_df = pd.DataFrame(st.session_state['project_history'])
        fig = px.bar(history_df, x='Nom', y='Score Carbone', color='Classification',
                     title="Comparaison des Scores Carbone",
                     color_discrete_map={'Vert': '#2e7d32', 'Acceptable': '#ff9800', 'Très polluant': '#d32f2f'})
        fig.update_layout(showlegend=True, xaxis_title="Projets", yaxis_title="Score Carbone (/100)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucun projet soumis pour le moment.")