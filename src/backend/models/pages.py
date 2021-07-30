from .base import CollectionBase

class Pages(CollectionBase):
	def __init__(self):
		super(Pages, self).__init__('Pages')
		self.required_fields.update(['image', 'name', 'owner'])
		self.optional_fields.update(
			verified=False,
			annotations=None,
			book_id=None
		)