from flask import Blueprint, request, redirect, url_for
from ..message import *
from ..models import *
from .response import response
import zipfile


book_blueprint = Blueprint('books', __name__, url_prefix='/books')
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

# dont use now
@book_blueprint.route('/update',methods=['POST'])
def update():
	json_data = request.json
	id = json_data['_id']
	json_data.pop('_id')
	
	if id is None:
		return error('Id field not found')
	
	return books.update(id, json_data)
	
	
# dont use now
@book_blueprint.route('/delete',methods=['DELETE'])
def delete():
	id = request.args.get('id', default=None, type=str)
	if id is None:
		return error('Missing id field')
	return books.delete(id)
	
	
# dont use now
@book_blueprint.route('/insert', methods=['POST'])
def insert():
	element = request.json
		
	return books.insert(element)


@book_blueprint.route('/cover', methods=['GET'])
def get_cover():
	id = request.args.get('id', default=None, type=str)
	if id is None:
		return error('Missing id field')
	
	book_found = bookImgs.find_by_id(id)
	if book_found['success']:
		return book_found['data']['thumbnail']
	return book_found
	
@book_blueprint.route('/upload', methods=['POST'])
def save_uploaded_zipfile():
	file = request.files['upload-file']  
	name = file.filename
	file_like_object = file.stream._file  
	zipfile_ob = zipfile.ZipFile(file_like_object)
	file_names = zipfile_ob.namelist()
	file_names = [file for file in file_names if file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS]
	
	files = [zipfile_ob.open(name).read() for name in file_names]
	
	upload = books.upload_book(name, files, file_names, users.who())
	
	return redirect(url_for('main_page'))