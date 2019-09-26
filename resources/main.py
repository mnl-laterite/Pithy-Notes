from flask_restful import Resource
from flask import render_template, make_response, redirect, Response, request
from flask_login import login_required, current_user
from .auth import db
import time
from bson import json_util, ObjectId

notes = db["Notes"]
users = db["Users"]


class Home(Resource):

    @staticmethod
    def get():
        if current_user.is_authenticated:
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('index.html'), 200, headers)
        else:
            return redirect('/login')


class Notes(Resource):

    @login_required
    def get(self):
        """ Get all notes by current user."""
        result = users.find_one({"Username": current_user.get_id()}, {"Notes.Contents": 0})["Notes"]
        return Response(json_util.dumps(result), mimetype='application/json')

    @login_required
    def post(self):
        """ Creates a new note for the current user."""
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
        data = request.get_json()
        search_string = None
        if data:
            search_string = data["Search"]

        if search_string:
            result = notes.find({"$or":
                                [{"Owner": current_user.get_id(),
                                  "Title": {"$regex": search_string, "$options": "i"}},
                                 {"Owner": current_user.get_id(),
                                  "Contents": {"$regex": search_string, "$options": "i"}}]})
        else:
            result = notes.find({"Owner": current_user.get_id()})

        return Response(json_util.dumps(result), mimetype='application/json')


class Note(Resource):

    @login_required
    def get(self, note_id):
        result = notes.find_one({"_id": ObjectId(note_id)})
        return Response(json_util.dumps(result), mimetype='application/json')

    @login_required
    def post(self, note_id):
        data = request.get_json()
        title = data["Title"]
        contents = data["Contents"]

        if title != "":
            users.update({"Username": current_user.get_id(), "Notes": {"$elemMatch": {"_id": ObjectId(note_id)}}},
                         {"$set": {"Notes.$.Title": title, "Notes.$.Contents": contents}})
            notes.update({"_id": ObjectId(note_id)}, {"$set": {"Title": title, "Contents": contents}})
        else:
            users.update({"Username": current_user.get_id(), "Notes": {"$elemMatch": {"_id": ObjectId(note_id)}}},
                         {"$set": {"Notes.$.Contents": contents}})
            notes.update({"_id": ObjectId(note_id)}, {"$set": {"Contents": contents}})

    @login_required
    def delete(self, note_id):
        notes.delete_one({"_id": ObjectId(note_id)})
        users.update({"Username": current_user.get_id()}, {"$pull": {"Notes": {"_id": ObjectId(note_id)}}})
