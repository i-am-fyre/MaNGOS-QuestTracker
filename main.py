from flask import Flask, jsonify, render_template, url_for
import requests
import configparser
import MySQLdb
from secrets import token_hex

app = Flask(__name__, static_folder='static', template_folder='templates')
config = configparser.ConfigParser()
config.read('config.ini')

app.secret_key = token_hex(16)

# Initialize database
db = MySQLdb.connect(host=config.get('Database', 'host'),
                        user=config.get('Database', 'user'),
                        password=config.get('Database', 'password'),
                        port=int(config.get('Database', 'port')),
                        database=config.get('Database', 'database'))

@app.route('/')
def index():
    response = requests.get('http://localhost:5000' + url_for('quest_tracker'))
    data = response.json()
    return render_template('index.html', data=data)

@app.route('/api/quest_tracker')
def quest_tracker():
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM quest_tracker')
    data = cursor.fetchall()
    return jsonify(data)
