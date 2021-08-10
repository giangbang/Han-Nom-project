from .base import CollectionBase
from bson import Binary


class Images(CollectionBase):
	def __init__(self):
		super(Images, self).__init__('Images')
		self.required_fields.update(['img'])

	def upload(self, file):
		
		binary_ = Binary(file)
		return self.insert({"img": binary_})
		
images = Images()