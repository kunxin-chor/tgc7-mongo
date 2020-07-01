from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv
import pymongo

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.environ.get('MONGO_URL')
DB_NAME = "sample_airbnb"

client = pymongo.MongoClient(MONGO_URI)

@app.route('/')
def show_listings():
    all_listings = client[DB_NAME].listingsAndReviews.find().limit(10)
    return render_template('show_listings.template.html', all_listings=all_listings)

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)