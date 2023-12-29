import sqlite3
from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)
DATABASE = 'tutorial.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Enables column access by name
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS movie (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year TEXT NOT NULL,
            score TEXT NOT NULL,
            created_at DATETIME NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM movie ORDER BY created_at DESC")
    movies = cur.fetchall()
    conn.close()
    return render_template('index.html', movies=movies)

@app.route('/add', methods=('GET', 'POST'))
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        score = request.form['score']
        created_at = datetime.datetime.now()
        conn = get_db_connection()
        conn.execute("INSERT INTO movie (title, year, score, created_at) VALUES (?, ?, ?, ?)",
                     (title, year, score, created_at))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_movie.html')

@app.route('/delete/<int:id>', methods=('POST',))
def delete_movie(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM movie WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
