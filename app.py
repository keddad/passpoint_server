from flask import Flask, jsonify, request, make_response, abort, Response, render_template
import logging
import os
import bson
from bson.binary import Binary
from bson.objectid import ObjectId
import datetime
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
signatures = client.signatures

logging.basicConfig(filename="log",
                    format='%(asctime)-6s: %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s',
                    level=logging.DEBUG)

app = Flask(__name__)


@app.route('/api/add_note', methods=['POST'])
def add_note():
    try:
        document = {
            "Place": request.form["Place"],
            "FirstName": request.form['firstName'],
            "MiddleName": request.form['middleName'],
            "LastName": request.form['lastName'],
            "Signature": {
                "Filename": "Signature",
                "Binary": Binary(request.form["signature"]),
                "MIME-Type": "image/png"
            }
            "AddTime": datetime.datetime.now()
        }
        signatures.insert_one(document)
    except:  # Need to find exceptions TODO
        logging.error(
            "Something went wrong on /api/add_note when parsing {}".format(request.json))
        abort(400)
    logging.info("Looks like /api/add_note processed normally")
    return Response(status=201)


@app.route('/get_render/<fileId>')
def return_render(fileId):
    logging.info(f"Got a /api/get_render/{fileId}/ request")
    try:
        query = {"_id": ObjectId(fileId)}
        post = signatures.find_one(query)
        return render_template("agreement_template.html", document=post)
    except Exception as e:
        return jsonify({"error": e})
        


@app.route('/download/<fileId>')
def download(fileId):
    try:
        query = {'_id': ObjectId(fileId)}
        doc = signatures.find_one(query)
        fileName = doc["Signature"]["Filename"]
        response = make_response(doc["Signature"]['Binary'])
        response.headers['Content-Type'] = doc["Signature"]["MIME-Type"]
        response.headers["Content-Dispostion"] = "attachment; filename=\"%s\"" % fileName
        return response
    except Exception as e:
        return jsonify({"error": e})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port='8080')
