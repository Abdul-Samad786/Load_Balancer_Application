import os
from flask import Flask
from routes.main import main_bp

def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    debug = os.getenv('FLASK_ENV', 'development') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=5000)
