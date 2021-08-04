from flask import Blueprint, request
from ..message import *
from ..models import users


user_blueprint = Blueprint('users', __name__, url_prefix='/users')

@user_blueprint.route('/update',methods=['POST'])
def update():
	json_data = request.json
	id = json_data['_id']
	json_data.pop('_id')
	
	if id is None:
		return error('Id field not found')
	
	return users.update(id, json_data)
	
	
@user_blueprint.route('/delete',methods=['DELETE'])
def delete():
	id = request.args.get('id', default=None, type=str)
	if id is None:
		return error('Missing id field')
	return users.delete(id)
	
@user_blueprint.route('/insert', methods=['POST'])
def insert():
	element = request.json
		
	return users.insert(element)
	
@user_blueprint.route('/login', methods=['POST'])
def login():
	element = request.json
	password = element['password']
	username = element['username']
	
	if not username or not password:
		return error('missing username or password.')
	return users.login(username, password)
	
@user_blueprint.route('/logout', methods=['GET'])
def logout():
	return users.logout()

@user_blueprint.route('/register', methods=['POST'])
def register():
	return users.register(request.json)

@user_blueprint.route('/who', methods=['GET'])
def who():
	return users.who()