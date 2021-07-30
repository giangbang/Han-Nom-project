from flask import Blueprint, request
from ..message import *
from ..models import pages


page_blueprint = Blueprint('pages', __name__, url_prefix='/pages')

@page_blueprint.route('/update',methods=['POST'])
def update():
	json_data = request.json
	id = json_data['_id']
	json_data.pop('_id')
	
	if id is None:
		return error('Id field not found')
	
	return pages.update(id, json_data)
	
	
@page_blueprint.route('/delete',methods=['DELETE'])
def delete():
	id = request.args.get('id', default=None, type=str)
	if id is None:
		return error('Missing id field')
	return pages.delete(id)
	
@page_blueprint.route('/insert', methods=['POST'])
def insert():
	element = request.json
		
	return pages.insert(element)
