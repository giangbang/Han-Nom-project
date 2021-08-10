from .base import CollectionBase
from .images import images

# {
	# bookId
	# page_number: 
	# annotations: [
		# {x,y,w,h}
	# ]
	# verified: 
	# imgId:
# }

class Pages(CollectionBase):
	def __init__(self):
		super(Pages, self).__init__('Pages')
		self.required_fields.update(['page_number', 'bookId', 'imgId'])
		self.optional_fields.update(
			verified=False,
			annotations=None,
		)
		
	def upload(self, page_img, bookId, page_number, **kwargs):
		insert_img = images.upload(page_img)
		if not insert_img['success']:
			return insert_img
		insert_img_id = insert_img['data']
		new_page = {
			'imgId': insert_img_id,
			'page_number': page_number,
			'bookId': bookId,
			**kwargs
		}
		return self.insert(new_page)

pages = Pages()