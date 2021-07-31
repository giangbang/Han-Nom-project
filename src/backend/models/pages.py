from .base import CollectionBase

class Pages(CollectionBase):
	def __init__(self):
		super(Pages, self).__init__('Pages')
		self.required_fields.update(['image', 'name'])
		self.optional_fields.update(
			verified=False,
			annotations=None,
		)
		
	def get_pages(page_ids: list):
		''' Get all the pages in a book, given the list of page ids.
		Since each page can be large, this funtion sequentially returns each page one after another.
		'''
		for id in page_ids:
			yield self.find_by_id(id)
			