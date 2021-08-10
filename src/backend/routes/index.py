from flask import Blueprint, render_template, redirect, request
from ..message import *
from ..models import *
from .response import response
from .render import *

indx_blueprint = Blueprint('', __name__)

@indx_blueprint.route('/', methods=['GET'])
def main_page():
	if not users.who(): 
		return redirect('/login')
	return render_index()

@indx_blueprint.route('/login', methods=['GET'])
def login():
	users.logout()
	return render_template('login.html')
	
@indx_blueprint.route('/register', methods=['GET'])
def register():
	users.logout()
	return render_template('register.html')

@indx_blueprint.route('/image', methods=['GET'])
def get_img():
	id = request.args.get('id', default=None, type=str)
	return images.find_by_id(id)['img']
	
@indx_blueprint.route('/book', methods=['GET'])
def read_book():
	id = request.args.get('id', default=None, type=str)
	return render_book(id)