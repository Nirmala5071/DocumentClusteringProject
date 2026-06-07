from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database Connection

def get_db():

    conn = sqlite3.connect("document.db")
    conn.row_factory = sqlite3.Row

    return conn


# Create Table

conn = get_db()

conn.execute("""
CREATE TABLE IF NOT EXISTS documents(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT
)
""")

conn.commit()


@app.route('/')
def home():

    return render_template('index.html')


@app.route('/upload', methods=['GET','POST'])
def upload():

    if request.method == 'POST':

        title = request.form['title']
        content = request.form['content']

        conn = get_db()

        conn.execute(
            """
            INSERT INTO documents
            (title,content)
            VALUES (?,?)
            """,
            (title,content)
        )

        conn.commit()

        return redirect('/documents')

    return render_template('upload.html')


@app.route('/documents')
def documents():

    conn = get_db()

    docs = conn.execute(
        """
        SELECT *
        FROM documents
        ORDER BY id DESC
        """
    ).fetchall()

    return render_template(
        'documents.html',
        documents=docs
    )


@app.route('/admin')
def admin():

    conn = get_db()

    total_docs = conn.execute(
        """
        SELECT COUNT(*)
        FROM documents
        """
    ).fetchone()[0]

    docs = conn.execute(
        """
        SELECT *
        FROM documents
        ORDER BY id DESC
        """
    ).fetchall()

    return render_template(
        'admin.html',
        total_docs=total_docs,
        documents=docs
    )


if __name__ == '__main__':

    app.run(debug=True)
