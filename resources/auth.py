from flask_restful import Resource
from flask import render_template, make_response, request, redirect, flash
from flask_login import UserMixin, login_user, logout_user, current_user, login_required
from pymongo import MongoClient
import bcrypt

client = MongoClient('mongodb://localhost:27017')
db = client.NotesDatabase
users = db["Users"]


class User(UserMixin):

    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username


class Register(Resource):

    @staticmethod
    def get():
        if current_user.is_authenticated:
            return redirect('/')
        # display the registration form
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('signup.html'), 200, headers)

    @staticmethod
    def post():
        username = request.form["Username"]
        password = request.form["Password"]
        password_repeat = request.form["PasswordRepeat"]

        # verifying validity of the data
        if password != password_repeat:
            flash("Please make sure your password is the same in both fields.")
            return redirect('/signup')

        # checking if the user already exists
        try:
            users.find({"Username": username})[0]
        except IndexError:
            # storing the user into the database
            hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
            users.insert_one({
                "Username": username,
                "Password": hashed_pw,
                "Notes": []
            })

            return redirect('/login')
        else:
            flash("Username already exists. Login or try a different one.")
            return redirect('/signup')


class Login(Resource):

    @staticmethod
    def get():
        if current_user.is_authenticated:
            return redirect('/')
        # display the log in form
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html'), 200, headers)

    @staticmethod
    def post():
        username = request.form["Username"]
        password = request.form["Password"]

        try:
            user = users.find({"Username": username})[0]
        except IndexError:
            flash("Could not find username. Please register or try again.")
            return redirect('/login')

        hashed_pw = user["Password"]
        if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
            user_obj = User(user["Username"])
            login_user(user_obj)
            return redirect('/')
        else:
            flash("Incorrect password. Please try again")
            return redirect('/login')


class Logout(Resource):

    @login_required
    def post(self):
        logout_user()
        return redirect('/login')
