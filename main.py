import os
from flask import Flask


app = Flask(__name__)
'test'

@app.route("/")
def hello():
    return "Congratulations, it's a web app!"