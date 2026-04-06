from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os
import shutil

app = Flask(__name__)
CORS(app)

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEPLOY_DB_PATH = os.path.join(BASE_DIR, 'links.db')
TEMP_DB_PATH = os.path.join('/tmp', 'links.db')


def is_writable_directory(path):
    return os.access(path, os.W_OK)


def get_database_path():
    if os.environ.get('VERCEL') == '1' or not is_writable_directory(BASE_DIR):
        if os.path.exists(DEPLOY_DB_PATH) and not os.path.exists(TEMP_DB_PATH):
            try:
                shutil.copyfile(DEPLOY_DB_PATH, TEMP_DB_PATH)
            except OSError:
                pass
        return TEMP_DB_PATH
    return DEPLOY_DB_PATH

DATABASE_PATH = get_database_path()


def get_db_connection():
    return sqlite3.connect(DATABASE_PATH)

def create_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY,
        video_title TEXT,
        video_link TEXT,
        video_thumbnail TEXT,
        tags TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY,
        name TEXT,
        picture TEXT
    )''')
    conn.commit()
    conn.close()

create_db()

@app.route('/')  #Decorator (which comes with function)
def welcome():
    return "This is starting page"

def get_links_with_titles():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT id, video_title, video_link, video_thumbnail, tags FROM videos')
    rows = c.fetchall()
    conn.close()
    links = [{'id': row[0], 'title': row[1], 'link': row[2], 'image_url': row[3], 'tags': row[4]} for row in rows]
    return jsonify(links)

# Define endpoint to fetch links with titles
@app.route('/get_links_with_titles')
def get_links_with_titles_and_images():
    try:
        return get_links_with_titles()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

   
@app.route('/get_names', methods=['GET'])
def get_names():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT id, name, picture FROM profiles')
    rows = c.fetchall()
    conn.close()
    names = [{'id': row[0], 'name': row[1], 'picture': row[2]} for row in rows]
    return jsonify(names)

@app.route('/profile/<int:profile_id>')
def get_profile(profile_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT id, name, picture FROM profiles WHERE id = ?', (profile_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify({'id': row[0], 'name': row[1], 'picture': row[2]})
    else:
        return jsonify({'error': 'Profile not found'}), 404

@app.route('/add_video', methods=['POST'])
def add_video():
    data = request.get_json()
    title = data.get('title')
    link = data.get('link')
    thumbnail = data.get('thumbnail')
    tags = data.get('tags')
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO videos (video_title, video_link, video_thumbnail, tags) VALUES (?, ?, ?, ?)', (title, link, thumbnail, tags))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Video added'})

@app.route('/add_profile', methods=['POST'])
def add_profile():
    data = request.get_json()
    name = data.get('name')
    picture = data.get('picture')
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO profiles (name, picture) VALUES (?, ?)', (name, picture))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Profile added'})

@app.route('/search_videos', methods=['GET'])
def search_videos():
    query = request.args.get('tags')
    if not query:
        return jsonify([])
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT id, video_title, video_link, video_thumbnail FROM videos WHERE tags LIKE ?', ('%' + query + '%',))
    rows = c.fetchall()
    conn.close()
    videos = [{'id': row[0], 'title': row[1], 'link': row[2], 'thumbnail': row[3]} for row in rows]
    return jsonify(videos)

if __name__ == '__main__':
    app.run(debug=True)
