from .base import CollectionBase
from flask import session
from ..message import *
from config import config as conf
from .books import books
from bson import ObjectId

import bcrypt

# {
	# username:
	# password:
# }

class Users(CollectionBase):
	def __init__(self):
		super(Users, self).__init__('Users')
		self.required_fields.update(['password', 'username'])
		
		
	def register(self, register_form: dict):
		'''
		Register new user into database, check if user already exists before being inserted.
		'''
		existing_user = self.collection.find_one({'username': register_form['username']})
		
		if existing_user is None:
			hashpass = bcrypt.hashpw(
				register_form['password'].encode(conf['encode-password']),
				bcrypt.gensalt())
			register_form['password'] = hashpass 
			return self.insert(register_form)
			
		return error('Username already exists!')
		
	def login(self, username:str, password:str):
		self.logout()
		if not username or not password:
			return error('missing username or password.')
		login_user = self.collection.find_one({'username': username})
		
		if login_user:
			if self.__compare_password(password, login_user['password']):
				session['id'] = str(login_user['_id'])
				return success(login_user)
				
		return error('Incorrect password or username!')	
		
	def isLogin(self):
		return session.get('id', None) is not None
		
	def logout(self):
		if 'id' in session:
			session.pop('id', None)
			return success('Logged out')
			
		return error('You are not logged in!')
			
	def __compare_password(self, password, hashpass):
		return hashpass == bcrypt.hashpw(
			password.encode(conf['encode-password']), 
			hashpass)
			
	def who(self):
		'''
		Return the current account id that is logged in
		'''
		return session.get('id', None)
		
	def get_books(self):
		userId = self.who()
		book_list = books.find({"userId": userId}, public_search=False)
		return book_list
		
users = Users()