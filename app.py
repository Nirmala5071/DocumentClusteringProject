from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(**name**)

# ==========================

# DATABASE CONNECTION

# ==========================

def get_db():

```
conn = sqlite3.connect("document.db")
conn.row_factory = sqlite3.Row

return conn
```

# ==========================

# CREATE TABLE

# ==========================

conn = get_db()

conn.execute("""
CREATE TABLE IF NOT EXISTS documents(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
topic TEXT,
content TEXT,
upload_date TEXT
)
""")

conn.commit()

# ==========================

# HOME PAGE

# ==========================

@app.route('/')
def home():

```
return render_template('index.html')
```

# ==========================

# UPLOAD DOCUMENT

# ==========================

@app.route('/upload', methods=['GET', 'POST'])
def upload():

```
if request.method == 'POST':

    title = request.form['title']
    topic = request.form['topic']
    content = request.form['content']

    upload_date = str(date.today())

    conn = get_db()

    conn.execute(
        """
        INSERT INTO documents
        (title,topic,content,upload_date)
        VALUES (?,?,?,?)
        """,
        (
            title,
            topic,
            content,
            upload_date
        )
    )

    conn.commit()

    return redirect('/documents')

return render_template('upload.html')
```

# ==========================

# VIEW DOCUMENTS

# ==========================

@app.route('/documents')
def documents():

```
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
```

# ==========================

# SEARCH DOCUMENTS

# ==========================

@app.route('/search', methods=['GET', 'POST'])
def search():

```
results = []

if request.method == 'POST':

    keyword = request.form['keyword']

    conn = get_db()

    results = conn.execute(
        """
        SELECT *
        FROM documents
        WHERE title LIKE ?
        OR topic LIKE ?
        OR content LIKE ?
        """,
        (
            '%' + keyword + '%',
            '%' + keyword + '%',
            '%' + keyword + '%'
        )
    ).fetchall()

return render_template(
    'search.html',
    results=results
)
```

# ==========================

# DOCUMENT CLUSTERS

# ==========================

@app.route('/clusters')
def clusters():

```
conn = get_db()

topics = conn.execute(
    """
    SELECT DISTINCT topic
    FROM documents
    """
).fetchall()

return render_template(
    'clusters.html',
    topics=topics
)
```

# ==========================

# ADMIN DASHBOARD

# ==========================

@app.route('/admin')
def admin():

```
conn = get_db()

total_docs = conn.execute(
    """
    SELECT COUNT(*)
    FROM documents
    """
).fetchone()[0]

total_clusters = conn.execute(
    """
    SELECT COUNT(DISTINCT topic)
    FROM documents
    """
).fetchone()[0]

common_topic = conn.execute(
    """
    SELECT topic,
           COUNT(*) total
    FROM documents
    GROUP BY topic
    ORDER BY total DESC
    LIMIT 1
    """
).fetchone()

recent_uploads = conn.execute(
    """
    SELECT COUNT(*)
    FROM documents
    WHERE upload_date = ?
    """,
    (str(date.today()),)
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
    total_clusters=total_clusters,
    common_topic=common_topic,
    recent_uploads=recent_uploads,
    documents=docs
)
```

# ==========================

# RUN APP

# ==========================

if **name** == '**main**':

```
app.run(debug=True)
```
