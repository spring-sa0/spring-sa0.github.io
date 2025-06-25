Guide d'Utilisation : Évaluation de l'Empreinte Carbone des Projets
Ce guide explique comment installer, configurer et utiliser l'application Streamlit développée pour évaluer l'empreinte carbone des projets soumis à une institution financière. L'application permet de calculer un score carbone, de classer les projets (Vert, Acceptable, Très polluant), de visualiser les impacts, et de générer des rapports PDF.
Prérequis

Python : Version 3.8 à 3.12 (vérifiez avec python --version).
Système d'exploitation : Windows, Linux, ou macOS.
Outils supplémentaires :
Un terminal (cmd/PowerShell pour Windows, Terminal pour Linux/macOS).
Git (optionnel, pour cloner un dépôt).
Une distribution LaTeX comme TeX Live (pour compiler le rapport final, optionnel).



Installation
1. Créer un dossier pour le projet
Créez un dossier pour organiser les fichiers du projet et naviguez dedans :
mkdir projet_carbone
cd projet_carbone

2. Créer un environnement virtuel
Pour isoler les dépendances, créez un environnement virtuel nommé venv :
python -m venv venv

Activez l'environnement virtuel :

Windows :venv\Scripts\activate


Linux/macOS :source venv/bin/activate



Vous devriez voir (venv) apparaître dans le terminal.
3. Installer les dépendances
Copiez le fichier requirements.txt suivant dans le dossier du projet :
streamlit==1.39.0
pandas==2.2.3
numpy==1.26.4
scikit-learn==1.5.2
plotly==5.24.1
reportlab==4.2.2

Installez les dépendances avec :
pip install -r requirements.txt

Vérifiez l'installation :
pip list

4. Configurer les fichiers du projet

Copiez le fichier app.py (code de l'application Streamlit) dans le dossier projet_carbone.
(Optionnel) Copiez rapport_final.tex si vous souhaitez compiler le rapport final.

Lancement de l'Application

Assurez-vous que l'environnement virtuel est activé.
Lancez l'application Streamlit :

streamlit run app.py


Une fenêtre de navigateur s'ouvrira automatiquement à l'adresse http://localhost:8501. Si ce n'est pas le cas, ouvrez cette URL manuellement.

Utilisation de l'Application
1. Navigation

Utilisez la barre latérale pour naviguer entre trois pages :
Soumettre un Projet : Formulaire pour évaluer un nouveau projet.
Historique des Projets : Liste des projets soumis avec filtres.
Comparaison des Projets : Graphique comparant les scores carbone.



2. Soumettre un Projet

Accédez à la page "Soumettre un Projet".
Remplissez le formulaire :
Nom du Projet : Entrez un nom unique.
Secteur : Choisissez parmi Construction, Transport, Industrie, Agriculture, ou Numérique.
Type d'Énergie : Sélectionnez Renouvelable, Mix, ou Fossile.
Type de Transport : Choisissez Local, Régional, ou International.
Matériaux Principaux : Sélectionnez Recyclé, Bois, ou Béton.
Durée du Projet : Ajustez la durée en mois (1 à 120).
Taille de l'Équipe : Ajustez le nombre de personnes (1 à 500).
Description (optionnel) : Uploadez un fichier PDF ou texte.


Cliquez sur Évaluer le Projet.
Consultez les résultats :
Score Carbone : Affiché avec une jauge (0 à 100).
Classification : Vert, Acceptable, ou Très polluant.
Facteurs Contributifs : Graphique en barres montrant l'impact de chaque critère.
Recommandations : Suggestions pour réduire l'empreinte carbone.


Téléchargez le rapport PDF avec le bouton Télécharger le Rapport PDF.

3. Historique des Projets

Accédez à la page "Historique des Projets".
Consultez la liste des projets soumis avec leurs détails (nom, secteur, score, classification, date).
Filtrez par secteur à l'aide du menu déroulant.

4. Comparaison des Projets

Accédez à la page "Comparaison des Projets".
Visualisez un graphique en barres comparant les scores carbone des projets, colorés selon leur classification.

Compilation du Rapport Final (Optionnel)
Si vous souhaitez compiler le rapport LaTeX (rapport_final.tex) :

Installez TeX Live :
Windows/macOS : Téléchargez depuis tug.org/texlive.
Linux : sudo apt-get install texlive-full (Ubuntu/Debian).


Naviguez dans le dossier du projet :cd projet_carbone


Compilez le rapport :latexmk -pdf rapport_final.tex


Ouvrez rapport_final.pdf pour consulter le rapport.

Dépannage

Erreur "Module not found" :
Vérifiez que l'environnement virtuel est activé.
Réinstallez les dépendances : pip install -r requirements.txt.


Streamlit ne s'ouvre pas :
Assurez-vous que le port 8501 est libre.
Essayez une autre commande : streamlit run app.py --server.port 8502.


Problèmes LaTeX :
Vérifiez que texlive-full et texlive-fonts-extra sont installés.
Assurez-vous que la police noto est disponible.


Questions : Consultez la documentation de Streamlit ou contactez le développeur.

Structure du Projet
projet_carbone/
│
├── venv/                  # Environnement virtuel
├── app.py                # Code principal de l'application Streamlit
├── requirements.txt      # Liste des dépendances
├── rapport_final.tex     # Rapport final en LaTeX (optionnel)
└── initialize.md         # Ce guide d'utilisation

Perspectives
Pour améliorer l'application, envisagez :

Intégration de bases de données réelles (ex. : ADEME, ecoinvent).
Analyse automatique des fichiers uploadés (ex. : via PyPDF2).
Déploiement sur un serveur cloud (ex. : Heroku, AWS).
Ajout d'animations avancées (ex. : Streamlit Lottie).

Ce guide vous permet de démarrer rapidement avec le projet. Pour des fonctionnalités avancées ou des personnalisations, consultez le rapport final ou contactez l'équipe de développement.