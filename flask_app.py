
# A very simple Flask Hello World app for you to get started with...
import pymysql
from flask import Flask
from flask import request, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config["DEBUG"] = True
mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'awanpc'
app.config['MYSQL_DATABASE_PASSWORD'] = 'awan1234'
app.config['MYSQL_DATABASE_DB'] = 'awanpc$buku'
app.config['MYSQL_DATABASE_HOST'] = 'awanpc.mysql.pythonanywhere-services.com'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def home():
    return '<h1>Web Service Unisbank !</h1><p>Latihan membuat API dengan Python dan Flask</p>'

@app.route('/books/', methods=['GET'])
def index():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        res = jsonify(rows)
        res.status_code = 200
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/create', methods=['POST'])
def create_books():
	try:
		_json = request.json
		_title = _json['title']
		_author = _json['author']
		_first_sentence = _json['first_sentence']
		_published = _json['published']

		# insert record in database
		sqlQuery = "INSERT INTO books(title) VALUES(%s)"
		data = (_title)
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(sqlQuery, data)
		conn.commit()
		res = jsonify('Books created successfully.')
		res.status_code = 200
		return res
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/books/<int:books_id>')
def books(books_id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM books WHERE id=%s", books_id)
		row = cursor.fetchone()
		res = jsonify(row)
		res.status_code = 200

		return res
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
