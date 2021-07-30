from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
from ..message import *

from ..config import conf


client = MongoClient(conf['url'])
db = client[conf['database']]

class CollectionBase(object):
	'''
	Collection base class.
	'''
	def __init__(self, collection_name: str):
		self.collection = db[collection_name]
		self.collection_name = collection_name
		self.required_fields = set()
		self.optional_fields = dict() # dictionary of field-default value pairs


	def insert(self, element)->(bool, str):
		'''
		Insert an element into this collection.
		Return a string representation of the id of the newly inserted element.
		Keyword arguments:
		element -- element to be inserted
		'''
		missing_fields = self.required_fields - element.keys()
		if len(missing_fields) > 0:
			return error('Fields missing :', list(missing_fields))

		element["created"] = datetime.now()
		element["updated"] = datetime.now()
		element = self.optional_fields.copy() | element
		inserted = self.collection.insert_one(element) 
		return success(str(inserted.inserted_id))

	def find(self, criteria, projection=None, sort=None, limit=0): 
		''' Find by criteria. '''
		if "_id" in criteria:
			criteria["_id"] = ObjectId(criteria["_id"])

		found = self.collection.find(filter=criteria, 
				projection=projection, limit=limit, sort=sort)
		found = list(found)
		for i in range(len(found)):  
			if "_id" in found[i]:
				found[i]["_id"] = str(found[i]["_id"])

		return success(found)

	def find_by_id(self, id):
		'''
		Find post in collection by id
		Return None if not found
		'''
		found = self.find({'_id':id}, limit=1) 
		
		if len(found) > 0:
			found = found[0]
			if "_id" in found:
				found["_id"] = str(found["_id"])
			return success(found)

		return error('Id not found')

	def update(self, id, element):
		'''
		Update already exist elements, by id
		Return True if success
		'''
		criteria = {"_id": ObjectId(id)}
		element["updated"] = datetime.now()
		set_obj = {"$set": element}  # update value

		updated = self.collection.update_one(criteria, set_obj)
		if updated.matched_count == 1:
			return success()
		else:
			return error('Cannot update')
		
	def delete(self, id):
		'''
		Delete element by id
		Return True if success
		'''
		try:
			id_obj = ObjectId(id)
		except:
			return error('Invalid id format')
		deleted = self.collection.delete_one({"_id": ObjectId(id)})
		if deleted.deleted_count == 1:
			return success()
		return error('id not found')
