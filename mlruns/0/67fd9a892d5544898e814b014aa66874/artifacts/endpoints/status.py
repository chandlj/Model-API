from src.core.endpoint import Endpoint

class Status(Endpoint):
    path = '/'

    def get(self):
        return 200
