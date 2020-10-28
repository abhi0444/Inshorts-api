# TODO: A lot to be done here.
# 1. Make Navigation bar responsive
# 2. Icons/Images for each category of news
# 3. Electron for making it an app


from flask import Flask, render_template, request

import api

app = Flask(__name__)
app.secret_key = "vjfubvnwiojbtg[[;[;wfhweufiwubke"


@app.route("/home")
@app.route("/")
def index():
    """
    This function should give the home page which is only
    for testing and no functionality from api is used here
    """
    return render_template("home.html")


@app.route("/news")
def news_home():
    """
    This function will return a response containing
    all the news from Inshorts and display it in browser
    """
    resp = (
        api.fetch_all()
    )  # Direct Return is not a good idea as it will cause the serer to
    # overload and thus fails , so first get the data and then move on
    category = "Top"
    return render_template("index.html", resp=resp, category=category, length = len(resp['data']))


@app.route("/news/<category>/<depth>", methods=["GET", "POST"])
def news(category,depth):
    """
    This function is also same but here category
    can be passed as well also this function makes
    use of the depth feature that helps in fetching
    more news
    """
    if request.method == "POST":
        depth = int(request.form["dep"])
        resp = api.fetch_category(category, depth)
    else:
        resp = api.fetch_category(category)

    return render_template("index.html", resp=resp, category=category, length = len(resp['data']))


if __name__ == "__main__":
    app.run(debug=True)
