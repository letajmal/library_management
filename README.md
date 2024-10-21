## /rent

```bash
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