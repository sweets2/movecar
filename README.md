# Should you move your car?

This is a web app that helps people park in the City of Hoboken, the 4th most densely populated city in America. Parking in Hoboken is difficult. The city of Hoboken has weekly street cleaning on every street and this means all parked cars have to move or they give out tickets! Hoboken is also at sea level which means minor thunderstorms causes flooding in certain areas and major storms flood many areas.

# Deployed here
https://python27392.pythonanywhere.com/

# The app

This web app gathers the user's location and tells them the relevant Hoboken street cleaning date/time, the precipitation amount, and whether they should move their car as a result. It was created to be useful to anybody who parks in the city of Hoboken and to demonstrate a live deployment with active users.

Here's how it works in more detail:
- Built with Python, Flask, and  JavaScript/HTML, the user clicks "update location" which gathers the user's current latitude/longitude. If the user is using wifi, the geolocation data won't be accurate enough. Thus, the user must confirm their location and cross streets manually with the dropdowns.
- The dropdowns will output the correct street cleaning dates and times. (Later, I will add functionality to so the geolocationwill automatically fill out the dropdowns.)
- Each unique user is given a unique session ID and latitude/longitude for their respective ID. These are stored until the user clicks "update location" again or clears their cookies.
- The app will automatically ensure the rules are consistent with any changes. Using Beautiful Soup, it scrapes the City of Hoboken municipal street cleaning rules. Python scripts automatically parse the raw data into usable data.
- The app also gets the current weather forecast with Openweathermap API, then checks for storms and warns the user they may need to move their car. Hoboken is at sea level so small thunderstorms can easily flood certain pockets of the city on certain blocks in the flood zone.

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

You will need to create your own API keys from Openweathermap.org, Googlemaps, and create your own Flask secret key in a .env file in the main directory first.

Example .env file:
```GOOGLE_MAPS_API_KEY='abcdefg123'
OPENWEATHERMAP_API_KEY='abcdefg123
SECRET_KEY='supersecretkey123'```

To run the project, use the following command in the virtual environment:
    ```
    python -m app.main
    ```

# Future Updates
Future updates will include:
1. Create tests. Refactor package and subpackage organization (separating 'routes' and 'main')
2. Check the location of the current street/day/time and tell the user if they're in violation, not just prompting the rules for the current street
3. Run webscraping automatically once a day to grab Hoboken street cleaning rules using Cron Jobs on PythonAnywhere
4. Move unique session data and latitude/longitude data to a database for scalability
5. Splitting the "update location" into two functions: "what's my current location", and "update location"
6. A front end and nicer landing page (interactive map overlay with rules listed on every street when zoomed)
7. Gather elevation data and warn user if they're in the flood zone. (E.G. Google: "Hoboken flood map")
8. Logic to presume the cross streets between the user (google/apple/bing map APIs don't have this feature)
9. More robust checks for outlier data, error handling, cross checking changes in data
10. Integration with City of Hoboken "Nixle" announcements related to parking/weather
11. Future city releases
