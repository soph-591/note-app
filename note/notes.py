from flask import Blueprint, flash, render_template, abort
from markdown import markdown

from note.db import get_db
from note.storage import load_upload

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
    if result is None:
        abort(404)
    md = load_upload(uuid, name)
    html = markdown(md, extensions=["extra", "sane_lists"])
    return render_template("note.html", content=html)
