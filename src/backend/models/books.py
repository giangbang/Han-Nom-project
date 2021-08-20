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
		
	def upload_book(self, name, files, filenames, userId):
		new_book = {"userId":userId, "name":name.rsplit('.', 1)[0]}		
		insert_book = self.insert(new_book)
		
		if not insert_book['success']:
			return insert_book
		insert_book_id = insert_book['data']
		cover_page_img_id = None
		
		for filename, file in zip(filenames, files):
			uploaded_page = pages.upload(file, insert_book_id, filename)
			if not cover_page_img_id:
				cover_page_img_id = uploaded_page['data']
		self.update(insert_book_id, {"cover_image_id":cover_page_img_id})
		return success("Upload book successfully")
		
books = Books()
