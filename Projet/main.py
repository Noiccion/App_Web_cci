from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask import request, redirect, url_for, render_template
import requests
from app import create_app, db

app = create_app()

app = Flask(__name__, template_folder='/home/lucas/Documents/project/app/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Task('{self.title}', '{self.description}', '{self.completed}')"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = Task(title=data['title'], description=data['description'], completed=data['completed'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Tâche créée avec succès !'})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return render_template('task_list.html', tasks=tasks)

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('task_detail.html', task=task)

@app.route('/tasks/<int:task_id>/edit', methods=['GET'])
def edit_task_form(task_id):
    # Récupérer la tâche à partir de la base de données ou renvoyer une erreur 404 si elle n'existe pas
    task = Task.query.get_or_404(task_id)
    # Renvoyer le formulaire de modification avec les détails de la tâche
    return render_template('task_modify.html', task=task)

@app.route('/tasks/<int:task_id>/edit', methods=['POST'])
def update_task(task_id):
    # Récupérer la tâche à partir de la base de données ou renvoyer une erreur 404 si elle n'existe pas
    task = Task.query.get_or_404(task_id)
    # Récupérer les données du formulaire
    data = request.form
    # Mettre à jour les attributs de la tâche avec les nouvelles valeurs
    task.title = data['title']
    task.description = data['description']
    # Si la case à cocher "completed" est cochée, définir le statut de la tâche sur True, sinon sur False
    task.completed = 'completed' in data
    # Enregistrer les modifications dans la base de données
    db.session.commit()
    # Rediriger l'utilisateur vers la page de détails de la tâche modifiée
    return redirect(url_for('get_task', task_id=task.id))


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Tâche supprimée avec succès !'})

@app.route('/weather', methods=['GET'])
def get_weather():
    # Faire appel à l'API de météo externe
    response = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=44.930953&lon=2.444997&appid=15b9018817dbfb2cf282ac8a2e78db55')
    weather_data = response.json()
    return render_template('weather.html', weather_data=weather_data)

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)

