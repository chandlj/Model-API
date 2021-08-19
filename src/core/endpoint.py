import os
from functools import wraps

from flask import request, jsonify, current_app, Response
from flask_restful import abort
import flask_restful
import jwt
from werkzeug.exceptions import HTTPException

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
        except HTTPException as e:
            raise e
        except Exception as e:
            current_app.logger.error(e)
            abort(Response(e.args, 500))

    return decorator

class Resource(flask_restful.Resource):
    method_decorators = [endpoint]

class Endpoint(Resource):
    path = None
    model_path = None
