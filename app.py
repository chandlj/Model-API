import os
from dotenv import load_dotenv
import importlib
import jwt

from src import app

load_dotenv()

os.environ['AUTH_TOKEN'] = jwt.encode(
    {"token": str(os.environ.get("SECRET_KEY"))}, "secret", algorithm="HS256"
)

app.run(debug=True)
