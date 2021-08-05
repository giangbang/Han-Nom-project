import os
import pymongo
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from flask_cors import CORS

from config import conf
from backend.routes import *

app = Flask(__name__, 
	template_folder=conf['template folder'], 
	static_folder=conf['static folder'])

CORS(app)
app.secret_key = conf['secret']

app.register_blueprint(page_blueprint)
app.register_blueprint(book_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(indx_blueprint)

if __name__ == '__main__':
   app.run(debug=conf['debug'])