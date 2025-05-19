# 🧠 Alzheimer Prediction

Ce projet vise à prédire la présence ou le stade de la maladie d'Alzheimer à l'aide d'algorithmes de **Machine Learning**, avec une interface utilisateur en **HTML/CSS/Bootstrap**, une base **Oracle** pour stocker les réponses et les résultats, et un tableau de bord **Power BI** pour visualiser les données. La méthodologie **CRISP-DM** a été utilisée pour structurer tout le projet.

---

## 🏗️ Architecture du projet

```mermaid
graph TD
    A[Interface Web - HTML/CSS/Bootstrap] --> B[Backend Python - Flask]
    B --> C[Modele ML entraine - joblib ou pickle]
    B --> D[Base Oracle]
    D --> E[Power BI]

Frontend : Formulaire web pour que l'utilisateur saisisse ses donnees
Backend : Recoit les donnees, predit avec le modele ML, enregistre dans Oracle
Base Oracle : Stocke les entrees utilisateurs et les predictions
Power BI : Se connecte a Oracle pour creer des dashboards dynamiques

🛠️ Technologies utilisées
Python, Scikit-learn, XGBoost – Machine Learning

HTML / CSS / Bootstrap – Interface utilisateur

cx_Oracle / SQLAlchemy – Connexion base Oracle

Oracle Database – Stockage structuré des données

Power BI – Visualisations des résultats

Jupyter Notebook – Modélisation et analyse exploratoire

✅ Fonctionnalités principales
📈 Suivi complet de la méthodologie CRISP-DM

🧠 Entraînement d’un modèle ML personnalisé

👨‍⚕️ Interface utilisateur responsive

🗄️ Enregistrement des réponses/prédictions dans Oracle

📊 Dashboard Power BI dynamique

🔍 Évaluation sur un dataset externe

🔄 Méthodologie : CRISP-DM
Compréhension métier

Compréhension des données

Préparation des données

Modélisation

Évaluation

Déploiement

📊 Résultats obtenus
Accuracy : 92.3 %

F1-score : 91.8 %

AUC-ROC : 0.95
(Évalué avec un dataset externe)

🗂️ Structure du projet
bash
Copier
Modifier
alzhimer-prediction/
│
├── interface_web/         # HTML, CSS, Bootstrap
├── notebooks/             # Notebooks Jupyter d'entraînement
├── model/                 # Modèle ML sauvegardé (joblib/pickle)
├── oracle/                # Scripts SQL et connexion à Oracle
├── powerbi/               # Rapport Power BI (.pbix)
├── backend/               # Scripts Python backend
├── app.py                 # Point d'entrée principal pour lancer l'application
├── requirements.txt       # Dépendances Python
└── README.md
🚀 Comment exécuter le projet
1. Cloner le dépôt
bash
Copier
Modifier
git clone https://github.com/bensidhomhadil/alzhimer-prediction.git
cd alzhimer-prediction
2. Installer les dépendances
bash
Copier
Modifier
pip install -r requirements.txt
3. Lancer l'application
bash
Copier
Modifier
python app.py
4. Visualisation Power BI
Ouvre le fichier Power BI powerbi/dashboard.pbix

Connecte-toi à ta base Oracle

Rafraîchis les données pour visualiser les résultats actuels

📚 Source des données
Dataset d'entraînement : Kaggle Alzheimer Dataset

Le modèle a été entièrement entraîné par mes soins
