import os
from flask import Flask

UPLOAD_FOLDER='uploads/'

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'note.sqlite'),
    )
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    os.makedirs(app.instance_path, exist_ok=True)

    from . import db
    db.init_app(app)

    from . import upload
    app.register_blueprint(upload.bp)

    from . import notes
    app.register_blueprint(notes.bp)

    return app
