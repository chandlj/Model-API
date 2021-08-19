import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Resource

import mlflow

from .core.endpoint import Endpoint
from src.server import Server

MODEL_PATH = 'src/models/trained_models'
SCALER_PATH = 'src/models/scalers'

def create_app():
    app = Flask(__name__)

    # # Setup App Context
    # app.config['MODEL_PATH'] = MODEL_PATH
    # app.config['SCALER_PATH'] = SCALER_PATH

    # if not os.path.exists(MODEL_PATH):
    #     os.mkdir(MODEL_PATH)
    
    # if not os.path.exists(SCALER_PATH):
    #     os.mkdir(SCALER_PATH)

    if not mlflow.get_experiment_by_name('Test'):
        mlflow.create_experiment('Test', 's3://mlflow')
    
    mlflow.set_experiment('Test')

    class Status(Resource):
        def get(self):
            return 200

    # Setup API with defualt status endpoint, scrape endpoints folder
    with app.app_context():
        server = Server(app)
        server.get_endpoints()
        server.add_resource(Status, '/status')
        # Endpoint.model_path = app.config['MODEL_PATH']

    CORS(app)

    return app

app = create_app()
