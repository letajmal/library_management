## /import_books

```bash
curl -X POST http://localhost:5000/import_books \
-H "Content-Type: application/json" \
-d '{"number_of_books": "5"}'
```

## /books

```bash

curl -X GET http://localhost:5000/books

curl -X POST http://localhost:5000/books \
-H "Content-Type: application/json" \
-d '{
      "book_id": 8598,
      "quantity": 2
}'

curl -X DELETE http://localhost:5000/books \
-H "Content-Type: application/json" \
-d '{
      "book_id": 8598,
      "quantity": 2
}'
```

## /members

```bash

curl -X GET http://localhost:5000/members

curl -X POST http://localhost:5000/members \
-H "Content-Type: application/json" \
-d '{"name": "bob"}'

curl -X DELETE http://localhost:5000/members \
-H "Content-Type: application/json" \
-d '{"member_id": "2"}'

```

## /rent

```bash

curl -X GET http://127.0.0.1:5000/rent

curl -X POST http://127.0.0.1:5000/rent \
-H "Content-Type: application/json" \
-d '[
    {
        "member_id": 43343,
        "rented_books": [
            {"book_id": 4225, "quantity": 2},
            {"book_id": 42545, "quantity": 1}
        ]
    }
]'

curl -X DELETE http://127.0.0.1:5000/rent \
-H "Content-Type: application/json" \
-d '[
    {
        "member_id": 43343,
        "rented_books": [
            {"book_id": 4225, "quantity": 1},
            {"book_id": 42545, "quantity": 1}
        ]
    }
]'

```