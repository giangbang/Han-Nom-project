from .base import CollectionBase
from .images import images
from .pages import pages
from ..message import *

# {
	# userId: 
	# name:
	# public: 
	# imgId: 
	# info: str
# }

class Books(CollectionBase):
	def __init__(self):
		super(Books, self).__init__('Books')
		self.required_fields.update(['userId', 'name'])
		self.optional_fields.update(
			public=False,
			info=None,
			cover_image_id=None
		)
		
	def find(self, criteria, public_search=True, *args, **kwargs):
		if public_search:
			criteria.update(public=True) # books that are public
		return super(Books, self).find(criteria, *args, **kwargs)
		
	def upload_book(self, name, files, filenames, userId, cover=True):
		new_book = {"userId":userId, "name":name.rsplit('.', 1)[0]}
		if cover:
			cover_img = files.pop(0)
			filenames.pop(0)
			insert_cover = images.upload(cover_img)
			if insert_cover['success']:
				cover_img_id = insert_cover['data']
				new_book.update(cover_image_id=cover_img_id)
		insert_book = self.insert(new_book)
		if not insert_book['success']:
			return insert_book
		insert_book_id = insert_book['data']
		for filename, file in zip(filenames, files):
			pages.upload(file, insert_book_id, filename)
		return success()
		
books = Books()
