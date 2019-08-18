from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Setup connection to mongodb
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Select database and collection to use
db = client.mars_db
collection = db.mars_info

@app.route("/")
def index():
    #listings = mongo.db.listings.find_one()
    return render_template('index.html')


@app.route("/scrape")
def scraper():
    #listings = mongo.db.listings
    mars_news = scrape_mars.scrape()
    #listings.update({}, listings_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
