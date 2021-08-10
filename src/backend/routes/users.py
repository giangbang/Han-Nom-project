from flask import Blueprint, request, redirect
from ..message import *
from ..models import users
from .response import response


user_blueprint = Blueprint('users', __name__, url_prefix='/users')

# dont use
@user_blueprint.route('/update',methods=['POST'])
def update():
	json_data = request.json
	id = json_data['_id']
	json_data.pop('_id')
	
	if id is None:
		return response(error('Id field not found'), False)
	
	return response(users.update(id, json_data), False)
	
#dont use
@user_blueprint.route('/delete',methods=['DELETE'])
def delete():
	id = request.args.get('id', default=None, type=str)
	if id is None:
		return error('Missing id field')
	return users.delete(id)
	
# dont use
@user_blueprint.route('/insert', methods=['POST'])
def insert():
	element = request.json
	return users.insert(element)

	
@user_blueprint.route('/login', methods=['POST'])
def login():
	element = request.get_json(force=True)
	password = element['password']
	username = element['username']
	ret = users.login(username, password)
	if ret['success']:
		return response('/', redirect=True)
	return response(ret['data'], False)
	
@user_blueprint.route('/logout', methods=['GET'])
def logout():
	return users.logout()

@user_blueprint.route('/register', methods=['POST'])
def register():
	res = users.register(request.get_json(force=True))
	if res['success']:
		return response('/', redirect=True)
	return response(res['data'], False)

@user_blueprint.route('/who', methods=['GET'])
def who():
	return users.who()