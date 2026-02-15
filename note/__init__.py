import os
from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'note.sqlite'),
    )
    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, "uploads")
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from . import db
    db.init_app(app)

    from . import upload
    app.register_blueprint(upload.bp)

    from . import notes
    app.register_blueprint(notes.bp)

    return app
