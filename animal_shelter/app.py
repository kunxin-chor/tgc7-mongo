from flask import Flask, render_template, request, redirect, url_for
import os
from bson.objectid import ObjectId
from dotenv import load_dotenv
import pymongo
import datetime

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.environ.get('MONGO_URL')
DB_NAME = "animal_shelter"

client = pymongo.MongoClient(MONGO_URI)


@app.route('/animals')
def show_all_animals():
    all_animals = client[DB_NAME].animals.find()
    return render_template('show_animals.template.html',
                           all_animals=all_animals)


@app.route('/animal/create')
def create_animal():
    all_animal_types = client[DB_NAME].animal_types.find()
    return render_template('create_animal.template.html',
                           all_animal_types=all_animal_types)


@app.route('/animal/create', methods=["POST"])
def process_create_animal():
    animal_name = request.form.get('animal_name')
    animal_type = request.form.get('animal_type')
    breed = request.form.get('breed')

    animal_type_object = client[DB_NAME].animal_types.find_one({
        "_id": ObjectId(animal_type)
    })

    client[DB_NAME].animals.insert_one({
        "name": animal_name,
        "type": {
            "_id": animal_type_object["_id"],
            "name": animal_type_object["type_name"]
        },
        "breed": breed
    })

    return "New animal saved"


@app.route('/animal/update/<id>')
def update_animal(id):
    # find the animal by its id
    # we must match by the ObjectId(...) object
    animal = client[DB_NAME].animals.find_one({
        "_id": ObjectId(id)
    })

    # get all animal types
    all_animal_types = client[DB_NAME].animal_types.find()

    return render_template("update_animal.template.html",
                           animal=animal,
                           all_animal_types=all_animal_types)


@app.route('/animal/update/<id>', methods=["POST"])
def process_update_animal(id):
    animal_name = request.form.get('animal_name')
    animal_type = request.form.get('animal_type')
    breed = request.form.get('breed')

    selected_animal_type = client[DB_NAME].animal_types.find_one({
        "_id": ObjectId(animal_type)
    })

    client[DB_NAME].animals.update_one({
        "_id": ObjectId(id)
    }, {
        "$set": {
            "name": animal_name,
            "type": {
                '_id': selected_animal_type["_id"],
                'name': selected_animal_type["type_name"]
            },
            "breed": breed
        }
    })

    return redirect(url_for('show_all_animals'))


@app.route('/animal/delete/<animal_id>')
def delete_animal(animal_id):
    animal = client[DB_NAME].animals.find_one({
        "_id": ObjectId(animal_id)
    })

    return render_template(
        'confirm_delete_animal.template.html',
        animal=animal)


@app.route('/animal/delete/<animal_id>', methods=["POST"])
def process_delete_animal(animal_id):
    client[DB_NAME].animals.remove({
        "_id": ObjectId(animal_id)
    })
    return redirect(url_for('show_all_animals'))


@app.route('/animal/<animal_id>/checkup/')
def show_animal_checkups(animal_id):
    animal = client[DB_NAME].animals.find_one({
        "_id": ObjectId(animal_id)
    })
    return render_template('checkup.template.html', animal=animal)


@app.route('/animal/<animal_id>/checkup/', methods=["POST"])
def process_add_checkup(animal_id):
    vet_name = request.form.get('vet-name')
    date = request.form.get('checkup-date')
    diagnosis = request.form.get('diagnosis')

    # convert the string of the data into an actual date object
    date = datetime.datetime.strptime(date, "%Y-%m-%d")

    client[DB_NAME].animals.update_one({
        "_id": ObjectId(animal_id),
    }, {
        "$push": {
            'checkups': {
                "_id": ObjectId(),
                "vet": vet_name,
                "date": date,
                "diagnosis": diagnosis
            }
        }
    })

    return redirect(url_for('show_animal_checkups', animal_id=animal_id))


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
