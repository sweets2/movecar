from flask import Flask, request, jsonify, render_template, session
from flask_apscheduler import APScheduler
import json
import uuid
from pathlib import Path
import sys
sys.path.append (str(Path(__file__).resolve().parent))
from app.config import get_secret_key, get_openweathermap_api_key, get_google_maps_api_key, get_arcgis_api_key
from app.scripts.weather_script import get_weather_forecast, open_forecast_file, check_lightrain_forecast, check_thunderstorm_forecast, today, tomorrow


class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

BASE_DIR = Path(__file__).resolve().parent


app.config['SECRET_KEY'] = get_secret_key()
google_key = get_google_maps_api_key()
openweather_key = get_openweathermap_api_key()
arcgis_key = get_arcgis_api_key()

parsed_hoboken_rules_file = BASE_DIR / 'data' / 'parsed_hoboken_rules.json' # Absolute path
user_data_file = BASE_DIR / 'data' / 'user_data.json' # Absolute path


# @app.before_first_request # pylint: disable=no-member
# def schedule_task():
#     """Run Openweather API get request every hour to get updated weather in JSON file."""
#     scheduler.add_job(id='hourly_update', func=get_weather_forecast(), trigger='interval', hours=1)



def load_hoboken_rules(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

hoboken_rules = load_hoboken_rules(parsed_hoboken_rules_file)

# Load weather scripts to parse JSON weather file
data = open_forecast_file()
check_thunderstorm_forecast = check_thunderstorm_forecast(data, today, tomorrow)
check_lightrain_forecast = check_lightrain_forecast(data, today, tomorrow)


def append_to_json(file_name, data):
    try:
        with open(file_name, "r", encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {}

    username = data['username'] # to be replaced with user login
    if username in existing_data:
        print(f"Overwriting data for user {username}")
    existing_data[username] = data

    with open(file_name, "w", encoding='utf-8') as json_file:
        json.dump(existing_data, json_file, indent=4)

@app.route('/')
def home():


    streets = []
    seen = set()
    for value in hoboken_rules:
        if value["Street"] not in seen:
            streets.append(value["Street"])
            seen.add(value["Street"])

    session_id = session.get('username', str(uuid.uuid4()))
    session['username'] = session_id

    try:
        with open(user_data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        user_data = data.get(session_id, {})
        street_address = data.get('street_address', None)
    except FileNotFoundError:
        street_address = None
    
    return render_template('index.html', streets=streets, street_address=street_address, arcgis_key=arcgis_key, 
                           check_thunderstorm_forecast= check_thunderstorm_forecast,
                           check_lightrain_forecast=check_lightrain_forecast)

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
    user_data = request.get_json()
    if 'username' not in session:
        session['username'] = str(uuid.uuid4().hex)  # Use a random session ID
    user_data['username'] = session['username']
    append_to_json(user_data_file, user_data)

    return jsonify({'status': 'success'}), 200

@app.route('/set_address', methods=['POST'])
def set_address():
    # session_id = session.get('username', None)
    # if not session_id:
    #     return jsonify({"status": "failed", "message": "Session ID not found"})

    # # new_data = request.json
    # # new_address = new_data.get('address', None)

    # # if new_address:
    # #     try:
    # #         with open(user_data_file, 'r', encoding='utf-8') as f:
    # #             data = json.load(f)
    # #     except FileNotFoundError:
    # #         data = {}
        
    # #     user_data = data.get(session_id, {})
    # #     user_data['address'] = new_address
    # #     data[session_id] = user_data

        # with open(user_data_file, 'w', encoding='utf-8') as f:
        #     json.dump(data, f)

    address = request.json.get('address', {})

    with open(user_data_file, 'w', encoding='utf-8') as f:
        json.dump(address, f)
    return jsonify({'status': 'success'})

@app.route('/get_addresses', methods=['GET'])
def get_addresses():
    # Read addresses from JSON file and return
    with open(user_data_file, 'w', encoding='utf-8') as f:
        addresses = json.load(f)
    return jsonify(addresses)



if __name__ == '__main__':
    # app.run
    app.run(host='127.0.0.1',port=5000,debug=True)