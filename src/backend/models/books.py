from .base import CollectionBase

class Books(CollectionBase):
	def __init__(self):
		super(Books, self).__init__('Books')
		self.required_fields.update(['owner'])
		self.optional_fields.update(
			thumbnail='default thumbnail image',
			public=False
		)
		
	def find(self, criteria, *args, **kwargs):
		criteria.update(public=True) # books that are public
		return super(Books, self).find(criteria, *args, **kwargs)
		