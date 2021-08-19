import mlflow
import pandas as pd
from flask import abort, jsonify, request, current_app, Response

from ..core.endpoint import Endpoint
from ..core import ValidationError

class ModelEndpoint(Endpoint):
    path = '/models/<string:model_id>'

    def get(self, model_id):
        '''
        Get a model
        '''
        try:
            model = mlflow.pytorch.load_model(f'{self.model_path}/{model_id}')
            return jsonify({'model': str(model)})
        except:
            abort(Response('Error retreiving model', 500))


    def post(self, model_id):
        '''
        Add a new model
        '''
        # TODO: Figure out how to add a new model properly
        if request.is_json:
            data = request.get_json()
            current_app.logger.info(data)
            try:
                model_name = data['name']
                model = data['model']
            except:
                raise ValidationError('Missing required body params')
            
            mlflow.pytorch.log_model(model, f'{model_id}', model_name)
        else:
            current_app.logger.error('Missing request body')
            abort(Response('Missing response body', 400))
        
        

    def update(self, model_id):
        '''
        Update an existing model
        '''
        pass
    
    def delete(self, model_id):
        '''
        Delete a model
        '''
        pass
