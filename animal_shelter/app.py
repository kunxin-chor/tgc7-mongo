from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv
import pymongo

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.environ.get('MONGO_URL')
DB_NAME = "animal_shelter"

client = pymongo.MongoClient(MONGO_URI)


@app.route('/animal/create')
def create_animal():
    return render_template('create_animal.template.html')


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)