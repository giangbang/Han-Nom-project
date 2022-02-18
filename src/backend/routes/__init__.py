from .pages import page_blueprint, page_blueprint_api
from .books import book_blueprint, book_blueprint_api
from .users import user_blueprint, user_blueprint_api
from .images import imgs_blueprint
from .index import indx_blueprint
from flask import Blueprint

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api_blueprint.register_blueprint(page_blueprint_api)
api_blueprint.register_blueprint(book_blueprint_api)
api_blueprint.register_blueprint(user_blueprint_api)
api_blueprint.register_blueprint(imgs_blueprint)


__all__ = ['page_blueprint', 'book_blueprint', 'user_blueprint', 'indx_blueprint', 'api_blueprint']