from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
import os
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'supersecretkey')

# Configuration de la base de données Oracle
username = 'SYSTEM'
password = 'hadil'
host = os.getenv('DB_HOST', 'localhost')
port = os.getenv('DB_PORT', '1521')
sid = os.getenv('DB_SID', 'xe')
app.config['SQLALCHEMY_DATABASE_URI'] = f'oracle+oracledb://{username}:{password}@{host}:{port}/{sid}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Définition des modèles
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, db.Sequence('USERS_ID_SEQ', schema='SYSTEM'), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Prediction(db.Model):
    __tablename__ = 'predictions'
    id = db.Column(db.Integer, db.Sequence('prediction_id_seq', schema='SYSTEM'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    education_level = db.Column(db.String(50))
    bmi = db.Column(db.Float)
    smoking = db.Column(db.Integer)
    alcohol_consumption = db.Column(db.Float)
    sleep_quality = db.Column(db.Float)
    family_history_of_alzheimers = db.Column(db.Integer)
    cardiovascular_disease = db.Column(db.Integer)
    diabetes = db.Column(db.Integer)
    depression = db.Column(db.Integer)
    hypertension = db.Column(db.Integer)
    cholesterol_total = db.Column(db.Float)
    mmse = db.Column(db.Float)
    functional_assessment = db.Column(db.Float)
    memory_complaints = db.Column(db.Integer)
    behavioral_problems = db.Column(db.Integer)
    adl = db.Column(db.Float)
    confusion = db.Column(db.Integer)
    disorientation = db.Column(db.Integer)
    personality_changes = db.Column(db.Integer)
    difficulty_completing_tasks = db.Column(db.Integer)
    forgetfulness = db.Column(db.Integer)
    prediction_result = db.Column(db.String(50))


# Fonction pour créer les tables
def create_tables():
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = inspect(engine)

    # Créer les tables si elles n'existent pas
    if not inspector.has_table("users"):
        User.__table__.create(bind=engine)
        print("Table 'users' créée.")
    else:
        print("Table 'users' existe déjà.")

    if not inspector.has_table("predictions"):
        Prediction.__table__.create(bind=engine)
        print("Table 'predictions' créée.")
    else:
        print("Table 'predictions' existe déjà.")


with app.app_context():
    create_tables()

# Charger le modèle de prédiction
model = joblib.load('random_forest_model.joblib')


# Routes
@app.route('/')
def home():
    return redirect(url_for('signin'))


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['first_name'] = user.first_name
            return redirect(url_for('profile'))
        else:
            flash('Identifiants incorrects. Veuillez réessayer.', 'danger')
    return render_template('signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Cet email est déjà utilisé. Veuillez en choisir un autre.', 'danger')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)

        new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Inscription réussie! Veuillez vous connecter.', 'success')
            return redirect(url_for('signin'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Erreur lors de l’inscription : {e}', 'danger')
    return render_template('signup.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # Récupérer les données saisies par l'utilisateur
        features = {
            'Age': request.form.get('age', type=int),
            'Gender': request.form.get('gender'),  # 'Male' ou 'Female'
            'EducationLevel': request.form.get('education_level', type=int),
            'BMI': request.form.get('bmi', type=float),
            'Smoking': request.form.get('smoking'),  # 'Oui' ou 'Non'
            'AlcoholConsumption': request.form.get('alcohol_consumption'),  # Plage de valeurs
            'SleepQuality': request.form.get('sleep_quality', type=float),
            'FamilyHistoryAlzheimers': request.form.get('family_history_of_alzheimers'),  # 'Oui' ou 'Non'
            'CardiovascularDisease': request.form.get('cardiovascular_disease'),  # 'Oui' ou 'Non'
            'Diabetes': request.form.get('diabetes'),  # 'Oui' ou 'Non'
            'Depression': request.form.get('depression'),  # 'Oui' ou 'Non'
            'Hypertension': request.form.get('hypertension'),  # 'Oui' ou 'Non'
            'CholesterolTotal': request.form.get('cholesterol_total', type=float),
            'MMSE': request.form.get('mmse', type=float),
            'FunctionalAssessment': request.form.get('functional_assessment', type=float),
            'MemoryComplaints': request.form.get('memory_complaints'),  # 'Oui' ou 'Non'
            'BehavioralProblems': request.form.get('behavioral_problems'),  # 'Oui' ou 'Non'
            'ADL': request.form.get('adl', type=float),  # Plage de valeurs
            'Confusion': request.form.get('confusion'),  # 'Oui' ou 'Non'
            'Disorientation': request.form.get('disorientation'),  # 'Oui' ou 'Non'
            'PersonalityChanges': request.form.get('personality_changes'),  # 'Oui' ou 'Non'
            'DifficultyCompletingTasks': request.form.get('difficulty_completing_tasks'),  # 'Oui' ou 'Non'
            'Forgetfulness': request.form.get('forgetfulness')  # 'Oui' ou 'Non'
        }

        # Convertir le genre : 'Male' -> 0, 'Female' -> 1
        if features['Gender'] == 'Male':
            features['Gender'] = 0
        elif features['Gender'] == 'Female':
            features['Gender'] = 1

        # Convertir les valeurs "Oui" en 1 et "Non" en 0 pour tous les champs Oui/Non
        yes_no_fields = [
            'Smoking', 'FamilyHistoryAlzheimers', 'CardiovascularDisease',
            'Diabetes', 'Depression', 'Hypertension', 'MemoryComplaints', 'BehavioralProblems',
            'Confusion', 'Disorientation', 'PersonalityChanges', 'DifficultyCompletingTasks', 'Forgetfulness'
        ]

        for field in yes_no_fields:
            if features[field] == 'Yes':
                features[field] = 1
            elif features[field] == 'No':
                features[field] = 0
            else:
                features[field] = 0  # En cas de valeur inattendue, on assigne 0 par défaut

        # Pour 'AlcoholConsumption' et 'ADL', on les laisse tels quels (valeurs numériques)
        features['AlcoholConsumption'] = request.form.get('alcohol_consumption', type=float)
        features['ADL'] = request.form.get('adl', type=float)

        # Création du DataFrame pour la prédiction
        X_new = pd.DataFrame([features], columns=features.keys())

        # Prédiction avec le modèle
        prediction = model.predict(X_new)

        # Enregistrer la prédiction dans la base de données
        user_id = session.get('user_id')
        if user_id:
            insert_prediction_to_db(user_id, features, prediction[0])

        # Renvoyer la page avec le résultat de la prédiction
        return render_template('profile.html', prediction=prediction[0])

    return render_template('profile.html')



def insert_prediction_to_db(user_id, features, prediction_result):
    # Créer un objet Prediction à partir des données et de la prédiction
    new_prediction = Prediction(
        user_id=user_id,
        age=features['Age'],
        gender=features['Gender'],  # Stocker 0 pour Male ou 1 pour Female
        education_level=features['EducationLevel'],
        bmi=features['BMI'],
        smoking=features['Smoking'],
        alcohol_consumption=features['AlcoholConsumption'],
        sleep_quality=features['SleepQuality'],
        family_history_of_alzheimers=features['FamilyHistoryAlzheimers'],
        cardiovascular_disease=features['CardiovascularDisease'],
        diabetes=features['Diabetes'],
        depression=features['Depression'],
        hypertension=features['Hypertension'],
        cholesterol_total=features['CholesterolTotal'],
        mmse=features['MMSE'],
        functional_assessment=features['FunctionalAssessment'],
        memory_complaints=features['MemoryComplaints'],
        behavioral_problems=features['BehavioralProblems'],
        adl=features['ADL'],
        confusion=features['Confusion'],
        disorientation=features['Disorientation'],
        personality_changes=features['PersonalityChanges'],
        difficulty_completing_tasks=features['DifficultyCompletingTasks'],
        forgetfulness=features['Forgetfulness'],
        prediction_result=str(prediction_result)  # Convertir en chaîne de caractères
    )

    db.session.add(new_prediction)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))


if __name__ == '__main__':
    app.run(debug=True)