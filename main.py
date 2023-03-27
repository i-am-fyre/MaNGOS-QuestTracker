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
                        port=int(config.get('Database', 'port')))

char_db = config.get('Database', 'char_database')
world_db = config.get('Database', 'world_database')


@app.route('/')
def index():
    response = requests.get('http://localhost:5000' + url_for('quest_tracker'))
    data = response.json()
    completed = {}
    abandoned = {}

    for quest in data:
        questId = quest['id']
        abandonedDate = quest['quest_abandon_time']
        completedDate = quest['quest_complete_time']

        # Check if the quest was completed
        if completedDate is not None:
            if questId not in completed or completedDate > completed[questId]:
                completed[questId] = completedDate

        # Check if the quest was abandoned
        if abandonedDate is not None:
            if questId not in abandoned or abandonedDate > abandoned[questId]:
                abandoned[questId] = abandonedDate

    # Merge the completed and abandoned dictionaries based on quest ID
    quests = {}
    for questId in set(list(completed.keys()) + list(abandoned.keys())):
        # Determine the quest's title
        q_cursor = db.cursor(MySQLdb.cursors.DictCursor)
        q_cursor.execute('SELECT Title FROM ' + world_db + '.quest_template WHERE entry = ' + str(questId))
        quest_name=q_cursor.fetchall()[0]['Title']

        quests[questId] = {'quest_name': quest_name, 'last_completed': completed.get(questId), 'last_abandoned': abandoned.get(questId)}

    # Count how many times the quest was completed and abandoned
    completed_count = {}
    abandoned_count = {}
    for questId, q in quests.items():
        completed_count[questId] = sum(1 for entry in data if entry['quest_complete_time'] is not None and entry['id'] == questId)
        abandoned_count[questId] = sum(1 for entry in data if entry['quest_abandon_time'] is not None and entry['id'] == questId)

    return render_template('index.html', completed_count=completed_count, abandoned_count=abandoned_count, quests=quests)

@app.route('/all')
def all_data():
    response = requests.get('http://localhost:5000' + url_for('quest_tracker'))
    data = response.json()
    return render_template('all.html', data=data)

@app.route('/api/quest_tracker')
def quest_tracker():
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM ' + char_db + '.quest_tracker')
    data = cursor.fetchall()
    return jsonify(data)
