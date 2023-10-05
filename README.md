# Should you move your car?

This web app helps people park in the City of Hoboken, the 4th most densely populated city in America. Parking in Hoboken is difficult! The city of Hoboken has weekly street cleaning on every street which gives tickets to cars parked on certain streets at certain times. Hoboken is also at sea level and so even minor storms will cause flooding in certain areas and can damages vehicles.

# Deployed here
https://movecar.pythonanywhere.com/

# The app

This web app gathers the user's location from their input and tells them the relevant Hoboken street cleaning date/time and the weather.

Here's how it works in more detail:
- Built with Python, Flask, and  JavaScript/HTML/CSS, the user clicks completes the dropdowns to output the correct street cleaning rules. The user can click the "find my location" button on the map which geolocates their current position. Works best with cellular, if the user is using wifi then the geolocation data won't be accurate enough.
- Each unique user is given a unique session ID and latitude/longitude for their respective ID. These are stored until the user clicks "update location" again or clears their cookies so the user can keep coming back to the tool without it resetting.
- The app will automatically ensure the rules are consistent with any changes. Using Beautiful Soup, it scrapes the City of Hoboken municipal street cleaning rules. Python scripts automatically parse the raw data into usable data.
- The app also gets the current weather forecast with Openweathermap API, then checks for storms and warns the user if there is a lot of rain.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/sweets2/movecar.git
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

You will need to create your own API keys from Openweathermap.org, Googlemaps, and create your own Flask secret key in a .env file in the main directory first. (Google maps will probably be removed in the future)

Example .env file:
GOOGLE_MAPS_API_KEY='abcdefg123'
ARCGIS_API_KEY='abcdefg123'
OPENWEATHERMAP_API_KEY='abcdefg123
SECRET_KEY='supersecretkey123'

To run the project, use the following command in the virtual environment:
    ```
    python -m app.main
    ```

# Future Updates
Future updates will include:
1. Create tests. Refactor package and subpackage organization (separating 'routes' and 'main')
2. Move unique session data and latitude/longitude data to a database for scalability
3. Overlay flood map on top of the navigation map and warn user if they're in the flood zone.
4. Logic to presume the cross streets between the user (google/apple/bing map APIs don't have this feature)
5. Unit testing and more robust checks for outlier data, error handling, etc
6. Integration with City of Hoboken "Nixle" announcements related to parking/weather
7. Use React as a front end and release as a mobile app. This allows the best feature of all - notifications if the user is in violation 24hr or 1hr before street cleaning or a big storm coming.
