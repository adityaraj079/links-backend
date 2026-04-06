import openpyxl
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'links.db')
XLSX_PATH = os.path.join(BASE_DIR, 'links-new.xlsx')


def create_db():
    conn = sqlite3.connect(DB_PATH)
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

wb = openpyxl.load_workbook(XLSX_PATH)
sheet = wb.active

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute('DELETE FROM videos')
c.execute('DELETE FROM profiles')

video_count = 0
profile_count = 0

for row in sheet.iter_rows(values_only=True):
    row = list(row) + [''] * 5
    name, link, picture, tags, title = row[:5]
    title = title.strip() if isinstance(title, str) else ''
    name = name.strip() if isinstance(name, str) else ''
    picture = picture.strip() if isinstance(picture, str) else ''
    link = link.strip() if isinstance(link, str) else ''
    tags = tags.strip() if isinstance(tags, str) else ''

    if title:
        c.execute(
            'INSERT INTO videos (video_title, video_link, video_thumbnail, tags) VALUES (?, ?, ?, ?)',
            (title, link, picture, tags)
        )
        video_count += 1
    elif name:
        c.execute(
            'INSERT INTO profiles (name, picture) VALUES (?, ?)',
            (name, picture)
        )
        profile_count += 1

conn.commit()
conn.close()

print(f"Database populated from Excel: {video_count} videos, {profile_count} profiles inserted.")
