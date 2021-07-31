from flask import Blueprint, request
from ..message import *
from ..models import books


book_blueprint = Blueprint('books', __name__, url_prefix='/books')

@book_blueprint.route('/update',methods=['POST'])
def update():
	json_data = request.json
	id = json_data['_id']
	json_data.pop('_id')
	
	if id is None:
		return error('Id field not found')
	
	return books.update(id, json_data)
	
	
@book_blueprint.route('/delete',methods=['DELETE'])
def delete():
	id = request.args.get('id', default=None, type=str)
	if id is None:
		return error('Missing id field')
	return books.delete(id)
	
@book_blueprint.route('/insert', methods=['POST'])
def insert():
	element = request.json
		
	return books.insert(element)
