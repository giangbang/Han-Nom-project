from .base import CollectionBase

class Books(CollectionBase):
	def __init__(self):
		super(Books, self).__init__('Books')
		self.required_fields.update(['owner', 'page_ids'])
		self.optional_fields.update(
			thumbnail='default thumbnail image',
			public=False
		)
		
	def find(self, criteria, *args, **kwargs):
		criteria.update(public=True) # books that are public
		return super(Books, self).find(criteria, *args, **kwargs)
		
	
	def get_books(book_ids: list):
	''' Get all the books in the given book ids list, useful when querying all user's books. '''
		for id in book_ids:
			yield self.find_by_id(id)