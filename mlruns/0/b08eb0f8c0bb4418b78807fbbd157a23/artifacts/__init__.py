import os
import importlib

from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api

import jwt

from src.server import Server

app = Flask(__name__)
app.config['SECRET_KEY'] = jwt.encode(
    {"token": str(os.environ.get("SECRET_KEY"))}, "secret", algorithm="HS256"
)

server = Server(app)
server.get_endpoints()

# TODO: Add CORS options
CORS(app)
