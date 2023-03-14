from flask import Flask
import configparser
import MySQLdb
from secrets import token_hex

app = Flask(__name__)
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
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM quest_tracker')
    data = cursor.fetchall()
    return str(data)