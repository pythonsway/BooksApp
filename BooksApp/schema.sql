CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
	password VARCHAR NOT NULL
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
	isbn VARCHAR NOT NULL,
	title VARCHAR NOT NULL,
	author VARCHAR NOT NULL,
	publication INTEGER NOT NULL
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
	book_id INTEGER REFERENCES books,
    user_id INTEGER REFERENCES users,
	rating INTEGER NOT NULL,
    review VARCHAR NOT NULL
);