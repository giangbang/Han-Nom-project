from .base import CollectionBase
from .images import images
from .pages import pages
from ..detectors.DB import *
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
        
        page_ids = []
        for filename, file in zip(filenames, files):
            print(type(file))
            uploaded_page = pages.upload(file, insert_book_id, filename)
            if uploaded_page['success']:
                page_ids.append(uploaded_page['data'])
                if not cover_page_img_id:
                    cover_page_img_id = uploaded_page['data']
        self.update(insert_book_id, {"cover_image_id":cover_page_img_id})
        return success(page_ids)
        
    def get_pages(self, bookid):
        pages_in_book = pages.find({"bookId":bookid}, sort={"page_number":1})
        return success(pages_in_book)
        
    def delete(self, id):
        if self.find_by_id(id):
            pages_in_book = pages.find({"bookId":id})
            deleted = super().delete(id)
            
            for page_in_book in pages_in_book:
                pages.delete(page_in_book['_id'])
            return deleted
        else:
            return error('Book {} not found.'.format(id))
            
    def detect_bboxes_and_save(self, page_ids, files):
        '''
        Detect bounding boxes of the given files (images).
        This routine is called everytime users upload new books.
        Arguments: 
        page_ids: ids of pages
        files: string images need to be detected
        id and file order should match each other
        '''
        res = detect_batch_image(files)
        ok = True
        for i, (page_id, bbox, shape) in enumerate(zip(page_ids, res['bbox'], res['shape'])):
            ok = ok & pages.update_bbox(page_id, bbox, shape)['success']
        if ok:
            return success("Done")
        return error("Something went wrong :v")
        
books = Books()
