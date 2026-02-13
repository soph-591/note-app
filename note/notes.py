from flask import Blueprint, flash, current_app, render_template
from note.db import get_db

from markdown import markdown

bp = Blueprint('notes', __name__)

@bp.route('/')
def index():
    db = get_db()
    files = db.execute(
            'SELECT id, created, name'
            ' FROM file'
            ' ORDER BY created DESC'
            ).fetchall()
    return render_template("index.html", files=files)

@bp.route('/notes/<int:id>', methods=['GET', 'POST'])
def render_note(id):
    db = get_db()
    result = db.execute(
            'SELECT uuid, name'
            ' FROM file'
            ' WHERE id == ?', (id,)
            ).fetchone()
    uuid, name = result
    upload_folder = current_app.config['UPLOAD_FOLDER']
    with open(f"{upload_folder}/{uuid}_{name}", "r") as f:
        md = f.read()
        return markdown(md)

#@bp.route('/notes/<int:id>/check', methods=['GET', 'POST'])
#def check(id):
#    db = get_db()
#    result = db.execute(
#            'SELECT uuid, name'
#            ' FROM file'
#            ' WHERE id == ?', (id,)
#            ).fetchone()
#    uuid, name = result
#    upload_folder = current_app.config['UPLOAD_FOLDER']
#    with open(f"{upload_folder}/{uuid}_{name}", "r") as f:
#        md = f.read()
