from flask import Flask, jsonify, request, make_response, abort
from peewee import *
from renderer import renderpdf
from models import SignedDocument, db

app = Flask(__name__)

db.connect()
db.create_tables([SignedDocument])

@app.errorhandler(400)
def bad_request():
    return make_response((jsonify({'error': 'Bad request'}), 404))


@app.route('/api/add_note', methods=['POST'])
def add_note():
    try:
        Document = SignedDocument(
            DeviceId=request.json['IdDevice'],
            FirstName=request.json['person']['firstName'],
            MiddleName=request.json['person']['middleName'],
            LastName=request.json['person']['lastName'],
            Signature=request.json['person']['signature']
        )
        Document.save()
    except: # Need to find exceptions TODO
        abort(400)


