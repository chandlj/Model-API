import os
from functools import wraps

from flask import request, jsonify
from flask_restful import Resource, abort
import jwt

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if os.environ['FLASK_ENV'] == 'development':
            return f(*args, **kwargs)

        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({
                'message': 'a valid token is missing'
            })

        try:
            decoded_token = jwt.decode(token, "secret", algorithms=["HS256"])
            decoded_key = jwt.decode(os.environ['AUTH_TOKEN'], "secret", algorithms=["HS256"])
            assert decoded_key == decoded_token
        except Exception as e:
            raise Exception from e

        return f(*args, **kwargs), 200
    return decorator

def endpoint(f):
    '''
    Wrapper for all endpoints. Handles error handling and response.
    '''
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            response = f(*args, **kwargs)
            return response
        except Exception as e:
            print(e)
            abort(500)

    return decorator

class Endpoint(Resource):
    method_decorators = [endpoint]
    path = None

class ModelEndpoint(Resource):
    method_decorators = [endpoint]
    path = None
    model = None
