from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from parslib.routes import main, auth, students
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(students.bp)

    return app