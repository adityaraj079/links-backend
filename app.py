from flask import Flask, jsonify
from openpyxl import load_workbook
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')  #Decorator (which comes with function)
def welcome():
    return "This is starting page"

# Define endpoint to fetch links with titles
@app.route('/get_links_with_titles')
def get_links_with_titles():
    # Load the Excel file
    wb = load_workbook('links-new.xlsx')
    ws = wb['Sheet1']

    # Extract links and titles from Excel
    links_with_titles = []
    for row in ws.iter_rows(values_only=True):
        # Check if the row has the expected number of columns
        if len(row) >= 2:
            links_with_titles.append({'link': row[1], 'title': row[0]})

    return jsonify(links_with_titles)

# Define endpoint to fetch names from the "profiles" sheet
def get_names():
    # Load the Excel file
    wb = load_workbook('links.xlsx')
    ws = wb['profiles']  # Assuming names sheet is named "profiles"

    # Extract names with URLs attached to their first
    names_with_urls = []
    for row in ws.iter_rows(values_only=True):
        if row[0]:  # Assuming each row has a name
            name_parts = row[0].split()  # Split the name into individual words
            hyphenated_name = '-'.join(name_parts)  # Join the words with hyphens
            url = f'https://www.pornhub.org/pornstar/{hyphenated_name}'  # Adjust the URL as needed
            name_with_url = {'name': row[0], 'url': url}
            names_with_urls.append(name_with_url)

    return jsonify(names_with_urls)

if __name__ == '__main__':
    app.run(debug=True)
