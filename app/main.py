import os
from flask import Flask, request, jsonify, render_template, session
import json
import uuid
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))
from app.config import get_secret_key, get_openweathermap_api_key, get_google_maps_api_key


app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

app.config['SECRET_KEY'] = get_secret_key()
google_key = get_google_maps_api_key()
openweather_key = get_openweathermap_api_key()

def append_to_json(file_name, data):
    try:
        with open(file_name, "r") as json_file:
            existing_data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {}

    username = data['username']
    if username in existing_data:
        print(f"Overwriting data for user {username}")
    existing_data[username] = data

    with open(file_name, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)

# Absolute path to parsed_hoboken_rules.json 
main_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
data_dir = os.path.join(main_dir,'data')
parsed_hoboken_rules_file = os.path.join(data_dir, 'parsed_hoboken_rules.json')  # Form the full path

# Absolute path to user_data.json
user_data_file = os.path.join(main_dir, 'user_data.json')


def load_hoboken_rules(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

hoboken_rules = load_hoboken_rules(parsed_hoboken_rules_file)

@app.route('/')
def home():
    streets = []
    seen = set()
    for value in hoboken_rules:
        if value["Street"] not in seen:
            streets.append(value["Street"])
            seen.add(value["Street"])
    return render_template('index.html', streets=streets)

@app.route('/get_side/<street>', methods=['GET'])
def get_side(street):
    relevant_data = [value for value in hoboken_rules if value["Street"] == street]
    side = list({value["Side"] for value in relevant_data})
    return jsonify({"side": side})

@app.route('/get_data/<street>/<side>', methods=['GET'])
def get_data(street, side):
    relevant_data = [value for value in hoboken_rules if value["Street"] == street and value["Side"] == side]
    locations = {value["Location"]: value["Days & Hours"] for value in relevant_data}
    return jsonify(locations)

@app.route('/get_rules/<street>/<side>/<location>', methods=['GET'])
def get_rules(street, side, location):
    for value in hoboken_rules:
        if value["Street"] == street and value["Side"] == side and value["Location"] == location:
            return jsonify({"days_hours": value["Days & Hours"]})

    return jsonify({"days_hours": "No rules found for the selected combination."})

@app.route('/location', methods=['POST'])
def update_location():
    """This is simulating a front end of an application which would take the user accurate geolocation,
    store that location, and check it against the street cleaning rules."""
    user_data = request.get_json()
    if 'username' not in session:
        session['username'] = str(uuid.uuid4().hex)  # Use a random session ID
    user_data['username'] = session['username']
    append_to_json(user_data_file, user_data)

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    # app.run
    app.run(host='127.0.0.1',port=5000,debug=True)