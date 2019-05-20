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
        document = SignedDocument(
            DeviceId=request.json['IdDevice'],
            FirstName=request.json['person']['firstName'],
            MiddleName=request.json['person']['middleName'],
            LastName=request.json['person']['lastName'],
            Signature=request.json['person']['signature']
        )
        document.save()
    except:  # Need to find exceptions TODO
        abort(400)
    return 201


@app.route('/api/get_render', methods=['GET'])
def return_render():
    try:
        document = SignedDocument.select().where(DeviceId=request.json["Id"]).get()
        rendered_document = renderpdf(document)
        with open("rendered_docs/{}.pdf".format(request.json["Id"]), 'w') as file:
            file.write(rendered_document)  # Not sure that it will work. Need to check. TODO
    except:
        abort(400)
    return 200


@app.route('/api/get_post', methods=['GET'])
def return_post():
    try:
        document = SignedDocument.select().where(DeviceId=request.json["Id"]).get()
        document_data = document.getdict()
        return jsonify(document_data), 200
    except:
        abort(400)