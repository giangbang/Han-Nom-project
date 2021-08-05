from flask import Blueprint, request, render_template
from ..message import *
from ..models import users

indx_blueprint = Blueprint('', __name__)

@indx_blueprint.route('/', methods=['GET'])
def main_page():
	if not users.who()['data']: 
		return render_template('login.html')
	return render_template('index.html')
