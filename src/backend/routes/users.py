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
