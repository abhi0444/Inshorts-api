"""
A lot to be done here.
1. Template for the start
2. Start page
3. Electron for making it an app
"""

from flask import Flask
import api

app = Flask(__name__)
app.secret_key = "vjfubvnwiojbtg[[;[;wfhweufiwubke"


@app.route("/home")
@app.route("/")
def index():
    return "Welcome to News and Weather app"


@app.route("/news")
def news_home():
    resp = api.fetch_all() # Direct Return is not a good idea as it will cause the serer to overload and thus fails , so first get the data and then move on
    return resp


@app.route("/news/<category>")
def news(category):
    resp = api.fetch_category(category)
    return resp

if __name__ == "__main__":
    app.run()
