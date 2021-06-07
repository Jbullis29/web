from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
#create an app in flask
app = Flask(__name__)
# connect my flask to mongo
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")
#crate a ne route in flask tha will render what I call from the database to the html
@app.route("/")
def index():
    # assign a variable to my database query to make typing easier
    info = mongo.db.articles.find_one()
    #telling flask to return my queries to my index file when I call articles 
    return render_template("index.html", articles=info)
# create another route on my html that when used directs you to the scrape mars code
@app.route("/scrape")
def scraper():
    #assigning everything that was scraped
    mars_data = scrape_mars.scrape()
    #inserting newly scraped data into my DB
    mongo.db.articles.update({}, mars_data, upsert=True)
    #once done redirect back to the home page
    return redirect("/")
#this allows flask to run and debug assigns pin for security
if __name__ == "__main__":
    app.run(debug=True)



