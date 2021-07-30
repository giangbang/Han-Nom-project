import os
import pymongo
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from flask_cors import CORS

from backend.routes import *

app = Flask(__name__, template_folder='./frontend')
CORS(app)
app.secret_key = os.urandom(12).hex()

app.register_blueprint(page_blueprint)

if __name__ == '__main__':
   app.run(debug=True)