from .books import Books
from .pages import Pages
from .users import Users

books = Books()
pages = Pages()
users = Users()

__all__ = ['books', 'pages', 'users']