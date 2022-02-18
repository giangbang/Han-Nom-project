from flask import Blueprint, render_template, redirect, request
from ..models import *


imgs_blueprint = Blueprint('image', __name__)

@imgs_blueprint.route('/get-image', methods=['GET'])
def get_img():
	id = request.args.get('id', default=None, type=str)
	return images.find_by_id(id)['img']
