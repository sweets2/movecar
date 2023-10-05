
existing_data = {
        "username": "6a972628-1f91-4580-954c-f1ca87d53580"
    }

data2 = {
    "6a972628-1f91-4580-954c-f1ca87d53580": {
        "latitude": 40.7732224,
        "longitude": -73.4298112,
        "username": "6a972628-1f91-4580-954c-f1ca87d53580"
    }
}


username = existing_data['username'] # to be replaced with user login
if username in existing_data:
    print(f"Overwriting data for user {username}")
# existing_data[username] = data



rain = ['a']

if not rain:
    print("List is empty")