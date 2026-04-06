import openpyxl
import sqlite3

# Load the Excel file
wb = openpyxl.load_workbook('links-new.xlsx')
sheet = wb.active

# Connect to the database
conn = sqlite3.connect('links.db')
c = conn.cursor()

# Assuming the Excel has columns: id, link, thumbnail, tags, title
for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip header
    if len(row) >= 5:
        id_val, link, thumbnail, tags, title = row[:5]
        if link and title:  # Only insert if link and title exist
            c.execute('INSERT INTO videos (video_title, video_link, video_thumbnail, tags) VALUES (?, ?, ?, ?)', (title, link, thumbnail or '', tags or ''))

conn.commit()
conn.close()

print("Database populated from Excel.")