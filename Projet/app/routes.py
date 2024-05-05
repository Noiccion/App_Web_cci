from flask import Blueprint, render_template
from .models import Task, db

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

