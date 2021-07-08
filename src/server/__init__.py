import os
import importlib
import inspect
import sys
from flask_restful import Api
from src.core.endpoint import Endpoint, ModelEndpoint

class Server(Api):
    def get_endpoints(self):
        paths = [
            entry.name.split('.py')[0]
            for entry in os.scandir('src/endpoints')
            if entry.is_file() and entry.name != '__init__.py'
        ]
        for path in paths:
            mod = importlib.import_module(f'.{path}', 'src.endpoints')
            for _, obj in inspect.getmembers(mod):
                if inspect.isclass(obj) and issubclass(obj, (Endpoint, ModelEndpoint)) and obj != Endpoint and obj != ModelEndpoint:
                    self.add_resource(obj, obj.path)
