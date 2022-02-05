# Installation
Download and install [mongodb](https://www.mongodb.com/), then open terminal and run the followings:

```sh
pip install -r requirements.txt
cd src
python app.py
```

# API TODO list

- [x] POST `/api/users/login`.
- [x] GET `/api/users/logout`.
- [x] GET `/api/users/who`, return current login username.
- [ ] POST `/api/books/cover?id={}`. Not needed for now.
- [x] GET `/api/users/get-books`, login required.
- [x] GET `/api/books/get-pages?id={}`, get all pages in a book.
- [ ] POST `/api/books/upload`, upload new book, login required. 
- [x] DELETE `/api/books/delete?id={}`, delete book, login required.

