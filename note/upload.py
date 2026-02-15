import os
from uuid import uuid4
from flask import Blueprint, request, flash, redirect, render_template
from werkzeug.utils import secure_filename

from note.db import get_db
from note.storage import save_upload

ALLOWED_EXTENSIONS = {'md'}

bp = Blueprint('upload', __name__)

def allowed_file(filename):
    extension = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and extension in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            safe_name = secure_filename(file.filename)
            uuid = uuid4()
            unique_filename = f"{uuid}_{safe_name}"
            save_upload(file, uuid, unique_filename)
            db = get_db()
            db.execute(
                'INSERT INTO file (uuid,name)'
                ' VALUES (?,?)',
                (str(uuid), safe_name)
            )
            db.commit()
            return redirect(request.url)
    return render_template("upload.html")
