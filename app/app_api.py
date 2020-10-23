"""
A lot to be done here.
1. Template for the start
2. Start page
3. Electron for making it an app
"""

from flask import Flask, render_template, request
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


@app.route("/news/<category>", methods=["GET","POST"])
def news(category):
    if request.method == "POST":
        depth = int(request.form["dep"])
        resp = api.fetch_category(category, depth)
        return render_template('depth.html', resp = resp)
    else:
        resp = api.fetch_category(category)
        return render_template('depth.html',resp = resp)

if __name__ == "__main__":
    app.run(debug=True)
