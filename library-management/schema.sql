DROP TABLE IF EXISTS books;

CREATE TABLE books (
    book_id VARCHAR(20) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    authors VARCHAR(255) NOT NULL,
    average_rating FLOAT,
    isbn VARCHAR(10),
    isbn13 VARCHAR(13),
    language_code CHAR(3),
    num_pages INTEGER,
    ratings_count INTEGER,
    text_reviews_count INTEGER,
    publication_date DATE,
    publisher VARCHAR(255),
    quantity INTEGER
);
<td>{{ book.bookID }}</td>
<td>{{ book.title }}</td>
<td>{{ book.authors }}</td>
<td>{{ book.average_rating }}</td>
<td>{{ book.isbn }}</td>
<td>{{ book.isbn13 }}</td>
<td>{{ book.language_code }}</td>
<td>{{ book.get('  num_pages') }}</td>
<td>{{ book.ratings_count }}</td>
<td>{{ book.text_reviews_count }}</td>
<td>{{ book.publication_date }}</td>
<td>{{ book.publisher }}</td>