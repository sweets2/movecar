"""This config file is the location for private keys to be sourced.
Env vars are kept privately on the machine hosting the web app, but referenced here.
Dotenv module is used to link the private key/values in the respective .env file or
elsewhere on the machine hosting the app."""
import os
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(name):
    """Get the environment variable or return exception"""
    try:
        return os.getenv(name)
    except KeyError as exc:
        error_msg = f"Missing expected environment variable {name}"
        raise EnvironmentError(error_msg) from exc

def get_arcgis_api_key():
    return get_env_variable('ARCGIS_API_KEY')

def get_google_maps_api_key():
    return get_env_variable('GOOGLE_MAPS_API_KEY')

def get_openweathermap_api_key():
    return get_env_variable('OPENWEATHERMAP_API_KEY')

def get_secret_key():
    return get_env_variable('SECRET_KEY')