from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
# PostgreSql connection
connection = psycopg2.connect(
    user = "postgres",
    password = "12345678",
    host = "localhost",
    port = "5432",
    database = "links_db")
cur = connection.cursor()

#Settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur.execute('SELECT * FROM links')
    data = cur.fetchall()
    return render_template('index.html', links = data)

@app.route('/add_link', methods=['POST'])
def add_link():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        cur.execute('INSERT INTO links (title, url) VALUES (%s, %s)', (title, url))
        connection.commit()
        flash('Link Added Successfully')
        return redirect(url_for('Index'))


@app.route('/edit/<id>')
def get_link(id):
    cur.execute('SELECT * FROM links WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edit_link.html', link = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_link(id):
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        cur.execute("""
            UPDATE links
            SET title = %s,
                url = %s
            WHERE id = %s
        """, (title, url, id))
        connection.commit()
        flash('Link Update Succesfully')
        return redirect(url_for('Index'))

@app.route('/delete/<int:id>')
def delete_link(id):
    cur.execute('DELETE FROM links WHERE id = {0}'.format(id))
    connection.commit()
    flash('Link Removed Succesfully')
    return redirect(url_for('Index'))