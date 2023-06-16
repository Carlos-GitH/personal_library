from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
db = SQLAlchemy(app)

#CREATES THE CLASS FOR THE TABLE ON ALCHEMY
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


#CREATES THE DATABASE AND ADD FIRST REGISTRY
# with app.app_context():
#     db.create_all()
#     new_book = Book(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
#     db.session.add(new_book)
#     db.session.commit()

#CREATES THE DATABASE WITH SQLITE3
# db = sqlite3.connect('books-collection.db')
# cursor = db.cursor()
# cursor.execute("""CREATE TABLE books (
#                     id INTEGER PRIMARY KEY,
#                     title varchar(250) NOT NULL UNIQUE,
#                     author varchar(250) NOT NULL,
#                     rating FLOAT NOT NULL)""")

#CREATES FIRST REGISTRY ON THE DATABASE WITH SQLITE3
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()

#HOME ROUTE
@app.route('/')
def home():
#QUERY ALL THE DATA IN THE DATABESE TO SHOW ON THE HOMEPAGE    
    with app.app_context():
        all_books = db.session.execute(db.select(Book)).scalars()
        return render_template('index.html', books=all_books)

#ROUTE FOR ADDING NEW BOOKS
@app.route("/add", methods=['GET', 'POST'])
#FUNCTION THAT CAPTURES THE VALUES FILLED IN THE FORM AND ADD TO THE DATABASE
def add():
    if request.method == 'POST':
        new_book = Book(
            title  = request.form['book'],
            author = request.form['author'],
            rating = request.form['rating']
        )
        with app.app_context():
            db.session.add(new_book)
            db.session.commit()        
        return redirect(url_for('home'))
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)

