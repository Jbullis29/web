from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route("/")
def index():
    info = mongo.db.articles.find_one()
    return render_template("index.html", articles=info)

@app.route("/scrape")
def scraper():
    mars_data = scrape_mars.scrape()
    mongo.db.articles.update({}, mars_data, upsert=True)
    return redirect("/")





if __name__ == "__main__":
    app.run(debug=True)



