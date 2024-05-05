from flask import jsonify, request
from main import app, db, Task, db_session

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    output = []
    for task in tasks:
        task_data = {'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed}
        output.append(task_data)
    return jsonify({'tasks': output})

@app.route('/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    task_data = {'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed}
    return jsonify(task_data)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = Task(titel=data['title'], description=data['description'], completed=data['completed'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Tâche créée avec succès !'})

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']
    db.session.commit()
    return jsonify({'message': 'Tâche mise à jour avec succès !'})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Tâche supprimée avec succès !'})