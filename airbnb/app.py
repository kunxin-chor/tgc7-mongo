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
    # get the current page number
    page_number = request.args.get('page')
    # if there is no page number (aka, None) then assume we are at page 0
    if page_number == None:
        page_number = 0
    else:
        page_number = int(page_number)

    print("page number=", page_number)
    all_listings = client[DB_NAME].listingsAndReviews.find().skip(
        page_number*20).limit(20)
    return render_template('show_listings.template.html',
                           all_listings=all_listings,
                           page_number=page_number)


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
