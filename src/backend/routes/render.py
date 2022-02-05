from flask import render_template, redirect
from ..models import *

def render_index():
	book_list = users.get_books()
	
	user = users.find_by_id(users.who(), {"username":1})
	if user is None:
		return redirect('/login')
	return render_template('index.html', books=book_list, username=user['username'])
	
def render_book(id):
	pages_in_book = pages.find({"bookId":id}, sort={"page_number":1})
	
	return render_template('read.html', pages=pages_in_book)