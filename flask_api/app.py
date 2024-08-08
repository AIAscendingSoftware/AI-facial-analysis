from flask import Flask
from flask_cors import CORS
from app.routes import main_bp
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, resources={r"/post_video": {"origins": "*"}})

    app.register_blueprint(main_bp)

    return app

def run_flask_app():
    app = create_app()
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])

if __name__ == '__main__':
    run_flask_app()