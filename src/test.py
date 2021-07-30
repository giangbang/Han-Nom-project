from pymongo import MongoClient

client = MongoClient('localhost')
db = client["han-nom"]

collection = db['pages']
collection.insert_many([
	{
		'faek': 'fwaef'
	}
])