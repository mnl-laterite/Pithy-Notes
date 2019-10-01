from flask_restful import Resource
from flask import render_template, make_response, redirect, Response, request
from flask_login import login_required, current_user
from .auth import db
import time
from bson import json_util, ObjectId

notes = db["Notes"]
users = db["Users"]


class Home(Resource):
    """ Resource class that handles main/index page view."""

    @staticmethod
    def get():
        """ Returns the home page view if the user is authenticated,
        redirects to the login page otherwise."""

        if current_user.is_authenticated:
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('index.html'), 200, headers)
        else:
            return redirect('/login')


class Notes(Resource):
    """ Resource class that handles the user notes retrieval, creation of a new note,
    and search API functions."""

    @login_required
    def get(self):
        """ Gets all the notes by the current user. Returns them in a JSON format.
        Note contents is withheld to improve performance/ease of transfer."""

        result = users.find_one({"Username": current_user.get_id()}, {"Notes.Contents": 0})["Notes"]
        return Response(json_util.dumps(result), mimetype='application/json')

    @login_required
    def post(self):
        """ Creates a new note for the current user using a default format.
        After creation returns the note so it can be rendered in the interface.
        Note fields are:
        Owner (the user who has made the note),
        Title (by default "New Note", the user may change it later),
        Time (the time at which the note was taken, in milliseconds from Unix Epoch),
        Contents (the text contents of the note, by default empty)."""

        time_from_epoch = int(round(time.time() * 1000))
        note = {
            "Owner": current_user.get_id(),
            "Title": "New Note",
            "Time": time_from_epoch,
            "Contents": "",
        }

        notes.insert_one(note)
        users.update({"Username": current_user.get_id()}, {"$push": {"Notes": note}})

        return Response(json_util.dumps(note), mimetype='application/json')

    @login_required
    def put(self):
        """ Search for the notes matching the search string.
        Expects a json with a "Search" field."""

        # get data
        data = request.get_json()

        # verify that data was indeed received in the correct format
        search_string = None
        if data:
            search_string = data["Search"]

        if search_string:
            # return all notes that match the search string in the title or contents
            result = notes.find({"$or":
                                [{"Owner": current_user.get_id(),
                                  "Title": {"$regex": search_string, "$options": "i"}},
                                 {"Owner": current_user.get_id(),
                                  "Contents": {"$regex": search_string, "$options": "i"}}]},
                                {"Contents": 0})
        else:
            # no search string was provided, so return all notes instead
            result = notes.find({"Owner": current_user.get_id()}, {"Contents": 0})

        return Response(json_util.dumps(result), mimetype='application/json')


class Note(Resource):
    """ Resource class that handles individual note retrieval, creation, and deletion API calls.
    Notes are handled by their unique ObjectId, provided in the URI string. """

    @login_required
    def get(self, note_id):
        """Retrieve the note with the given id from the database."""

        result = notes.find_one({"_id": ObjectId(note_id)})
        return Response(json_util.dumps(result), mimetype='application/json')

    @login_required
    def post(self, note_id):
        """Save/update the note with the given id to the database.
        If the provided id is "null", create a new note instead.
        Expects a JSON with "Title" and "Contents" fields."""

        # get the data
        data = request.get_json()
        title = data["Title"]
        contents = data["Contents"]

        if note_id == "null":
            # create a new note with the provided data and save it
            time_from_epoch = int(round(time.time() * 1000))
            note = {
                "Owner": current_user.get_id(),
                "Title": title,
                "Time": time_from_epoch,
                "Contents": contents
            }

            notes.insert_one(note)
            users.update({"Username": current_user.get_id()}, {"$push": {"Notes": note}})

            return Response(json_util.dumps(note), mimetype='application/json')

        if title != "":
            # a title was also provided, so update both note title and contents
            users.update({"Username": current_user.get_id(), "Notes": {"$elemMatch": {"_id": ObjectId(note_id)}}},
                         {"$set": {"Notes.$.Title": title, "Notes.$.Contents": contents}})
            notes.update({"_id": ObjectId(note_id)}, {"$set": {"Title": title, "Contents": contents}})
        else:
            # no title was provided, so update only note contents
            users.update({"Username": current_user.get_id(), "Notes": {"$elemMatch": {"_id": ObjectId(note_id)}}},
                         {"$set": {"Notes.$.Contents": contents}})
            notes.update({"_id": ObjectId(note_id)}, {"$set": {"Contents": contents}})

    @login_required
    def delete(self, note_id):
        """ Delete the note with the given id from the database. """

        notes.delete_one({"_id": ObjectId(note_id)})
        users.update({"Username": current_user.get_id()}, {"$pull": {"Notes": {"_id": ObjectId(note_id)}}})
