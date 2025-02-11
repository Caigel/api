from flask import Flask, request 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return {"books": [{"id": book.id, "book_name": book.book_name, "author": book.author, "publisher": book.publisher} for book in books]}

@app.route('/books', methods=['POST'])
def create_book():
    data = request.json
    new_book = Book(book_name=data['book_name'], author=data['author'], publisher=data['publisher'])
    db.session.add(new_book)
    db.session.commit()
    return {"message": "Book created successfully", "book": {"id": new_book.id, "book_name": new_book.book_name, "author": new_book.author, "publisher": new_book.publisher}}

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return {"id": book.id, "book_name": book.book_name, "author": book.author, "publisher": book.publisher}

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    book = Book.query.get_or_404(book_id)
    book.book_name = data['book_name']
    book.author = data['author']
    book.publisher = data['publisher']
    db.session.commit()
    return {"message": "Book updated successfully"}

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return {"message": "Book deleted successfully"}

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
