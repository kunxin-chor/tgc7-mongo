# Setup
from flask import Flask, render_template, request, redirect, url_for
import flask_login
import pymongo
import os
from dotenv import load_dotenv

# load variable sfrom .env into the environment
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

# initialise Mongo
client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
DB_NAME = 'my_app'

# Create the login manager and assign to our Flask app
login_manager = flask_login.LoginManager()
# tell Flask to use the Flask-Login's login manager
login_manager.init_app(app)


# User object
# The user object basically represents one user
class User(flask_login.UserMixin):
    pass


# user loader for the Flask-Login login manager
@login_manager.user_loader
def user_loader(email):
    # find the user from the database by its email
    user_in_db = client[DB_NAME].users.find_one({
        "email": email
    })
    print(user_in_db)
    if user_in_db:
        # create a new user object
        user = User()
        # set the id of the user object to be the user's email
        user.id = user_in_db['email']
        return user
    else:
        return None


# Our routes can begin here
@app.route('/register')
def register():
    return render_template('register.template.html')


@app.route('/register', methods=['POST'])
def process_register():
    client[DB_NAME].users.insert_one({
        'username': request.form.get('user-name'),
        'email': request.form.get('user-email'),
        'password': request.form.get('user-password')
    })

    return "new user has been created"


@app.route('/login')
def show_login_form():
    return render_template('login_form.template.html')


@app.route('/login', methods=["POST"])
def process_login():
    # grab the user from the db by email
    user_in_db = client[DB_NAME].users.find_one({
        'email': request.form.get('user-email')
    })

    if user_in_db:
        user = User()
        user.id = user_in_db['email']
        print(user)
        print(user.id)
        if request.form.get('user-password') == user_in_db['password']:
            flask_login.login_user(user)
            return "logged in successfully"
        else:
            return "wrong password"

    else:
        return "user's email not found in system"


@app.route('/restricted_page')
@flask_login.login_required
def my_secret_page():
    return "Restricted Area Entered"


@app.route('/profile')
def profile():
    return flask_login.current_user.id


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return "logged out"


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
