from .base import CollectionBase
from flask import session
from ..message import *
from ..config import conf

import bcrypt

class Users(CollectionBase):
	def __init__(self):
		super(Users, self).__init__('Users')
		self.required_fields.update(['password', 'username', 'book_ids'])
		
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
		login_user = self.collection.find_one({'username': username})
		
		if login_user:
			if self.__compare_password(password, login_user['password']):
				session['username'] = username
				return success('Logged in as ' + username)
				
		return error('Incorrect password or username!')	
		
	def logout(self):
		if 'username' in session:
			session.pop('username', None)
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
		return success(session.get('username', None))