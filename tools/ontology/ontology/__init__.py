from flask import Flask
from flask_cors import CORS
import requests

app = Flask(__name__)

CORS(app, supports_credentials=True)

from route import route

if __name__ == '__main__':
    app.run()
