from flask_restful import Resource
from flask import render_template, make_response, request, redirect, flash
from flask_login import UserMixin, login_user, logout_user, current_user, login_required
from pymongo import MongoClient
import bcrypt

client = MongoClient('mongodb://localhost:27017')
db = client.NotesDatabase
users = db["Users"]


class User(UserMixin):
    """ User class. Extends the UserMixin class from the Flask-Login module.
    Uses the username as the user id under the assumption that all username entries are unique."""

    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username


class Register(Resource):
    """ Resource class for handling user registration. """

    @staticmethod
    def get():
        """ Returns the sign-up view if the user is not authenticated,
        or redirects to the home page otherwise."""

        if current_user.is_authenticated:
            # user is authenticated already
            return redirect('/')

        # display the registration form
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('signup.html'), 200, headers)

    @staticmethod
    def post():
        """ Registers a user if the provided credentials are valid.
        Expects data from a form on the sign-up page found at templates/signup.html
        Form input field names should be: Username, Password, PasswordRepeat."""

        # get data
        username = request.form["Username"]
        password = request.form["Password"]
        password_repeat = request.form["PasswordRepeat"]

        # verify validity of the data
        if password != password_repeat:
            flash("Please make sure your password is the same in both fields.")
            return redirect('/signup')

        # check if the user already exists
        try:
            users.find({"Username": username})[0]
        except IndexError:
            # the username is not taken, so store the user into the database after encrypting the password
            hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
            users.insert_one({
                "Username": username,
                "Password": hashed_pw,
                "Notes": []
            })

            return redirect('/login')
        else:
            # username is taken, so notify the user about this and redirect to the sign-up page
            flash("Username already exists. Login or try a different one.")
            return redirect('/signup')


class Login(Resource):
    """ Resource class for handling user login/authentication."""

    @staticmethod
    def get():
        """ Returns the login view if the user is not authenticated,
        or redirects to the home page otherwise."""

        if current_user.is_authenticated:
            # user is already authenticated
            return redirect('/')

        # display the log in form
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html'), 200, headers)

    @staticmethod
    def post():
        """ Authenticates a user if the provided credentials are valid.
        Expects data from a form found at templates/login.html.
        Form input field names should be: Username, Password."""

        # get data
        username = request.form["Username"]
        password = request.form["Password"]

        # verify that user exists/is registered
        try:
            user = users.find({"Username": username})[0]
        except IndexError:
            flash("Could not find username. Please register or try again.")
            return redirect('/login')

        # verify that the provided password is correct
        hashed_pw = user["Password"]
        if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
            # the password matches, so authenticate the user and redirect to the home page
            user_obj = User(user["Username"])
            login_user(user_obj)
            return redirect('/')
        else:
            flash("Incorrect password. Please try again")
            return redirect('/login')


class Logout(Resource):
    """ Resource class for handling user de-authentication/logout function."""

    @login_required
    def post(self):
        logout_user()
        return redirect('/login')
