============================= test session starts ==============================
platform darwin -- Python 3.13.7, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/drewlarso/school/3150/testing-with-doubles-drewlarso
plugins: describe-2.2.0, mock-3.15.1, spec-5.1.0
collected 15 items

test_squirrel_server.py:

Squirrel Server Handler:

Create squirrels:
✓ It queries db to create squirrel with given data attributes

Handle methods:
✓ It handles squirrels index
✓ It handles squirrels retrieve on existing squirrel
✓ It handles squirrels retrieve on nonexisting squirrel
✓ It handles squirrels create
✓ It handles squirrels update existing
✓ It handles squirrels update nonexisting
✓ It handles squirrels delete existing
✓ It handles squirrels delete nonexisting
✓ It handles 404

Retrieve squirrels functionality:
✓ It queries db for squirrels
✓ It returns 200 status code
✓ It sends json content type header
✓ It calls end headers
✓ It returns response body with squirrels json data

============================== 15 passed in 0.05s ==============================
