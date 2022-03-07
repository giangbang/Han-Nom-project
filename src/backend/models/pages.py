from .base import CollectionBase
from .images import images
from ..message import *

# {
    # bookId
    # page_number: 
    # annotations: [
        # [[x0,y0], [x1,y1], [x2,y2], [x3,y3]],
        # [...]
    # ]
    # size: [w, h]
    # verified: 
    # imgId:
    # labels: [[top 5], []]
# }

class Pages(CollectionBase):
    def __init__(self):
        super(Pages, self).__init__('Pages')
        self.required_fields.update(['page_number', 'bookId', 'imgId'])
        self.optional_fields.update(
            verified=False,
            annotations=None,
            size=[0,0],
            labels=[]
        )
        
    def delete(self, id):
        deleted_page = self.find_by_id(id)
        if deleted_page:
            images.delete(deleted_page['imgId'])
            return super().delete(id)
        return error("Page {} not found".format(id))
        
    def update_bbox_and_label(self, id, bbox, shape, labels):
        return pages.update(id, {"annotations": bbox, "size": shape, "labels": labels})
    
    def update_bbox(self, id, bbox, shape):
        return pages.update(id, {"annotations": bbox, "size": shape})
    
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
        ok = self.insert(new_page)
        if ok['success']:
            return success([insert_img_id, ok['data']])
        return error("Something went wrong went inserting pages")

pages = Pages()