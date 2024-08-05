import os
from flask import Flask, render_template
from extensions import db
from routes.home_routes import home_bp
from routes.subject_routes import subject_bp
from routes.trainer_routes import trainer_bp
from routes.training_routes import training_bp
from routes.summary_routes import summary_bp

def create_app():
    app = Flask(__name__)
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'training_bugs.db')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key_here'

    db.init_app(app)

    app.register_blueprint(home_bp)
    app.register_blueprint(subject_bp)
    app.register_blueprint(trainer_bp)
    app.register_blueprint(training_bp)
    app.register_blueprint(summary_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    
