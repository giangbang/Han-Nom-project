from .base import CollectionBase
from flask import session
import bcrypt

class Users(CollectionBase):
	def __init__(self):
		super(User, self).__init__('Users')
		self.required_fields.update(['password', 'name', 'book_ids'])
		
	def register(self, register_form: dict):
		'''
		Register new user into database, check if user already exists before being inserted.
		'''
		existing_user = self.collection.find_one({'name': register_form['name']})
		
		if existing_user is None:
			hashpass = bcrypt.hashpw(register_form['password'], brypt.gensalt())
			register_form['password'] = hashpass 
			self.insert(register_form)
			return success()
		return error('Username already exists!')
		
	def login(username:str, password:str):
		login_user = self.find_one({'name': username})
		
		if login_user:
			if self.__compare_password(password, login_user['password']):
				session['username'] = username
				return success('Logged in as ' + username)
		return error('Incorrect password or username!')	
		
	def logout(username: str):
		if username in session:
			session.pop('username', None)
			return success('Logged out')
		return error('You are not logged in!')
			
	def __compare_password(password, hashpass):
		return hashpass == bcrypt.hashpw(password, hashpass)