import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from flask import current_app, request

from ..core.endpoint import Endpoint

class PredictEndoint(Endpoint):
    path = '/models/<string:model_id>/predict'

    def get(self, model_id):
        if request.is_json:
            data = request.get_json()
            df = pd.read_json(data)

        model = mlflow.pytorch.load_model(
            f'models:/{model_id}/none'
        )

        # TODO: Implement prediction
        # prediction = model()
