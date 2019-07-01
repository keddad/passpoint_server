from flask import Flask, jsonify, request, make_response, abort, Response, render_template
import logging
import os
import bson
from bson.binary import Binary
from bson.objectid import ObjectId
import datetime
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
signatures = client.db.signatures

logging.basicConfig(filename="log",
                    format='%(asctime)-6s: %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s',
                    level=logging.DEBUG)

app = Flask(__name__)


@app.route('/api/add_note', methods=['POST'])
def add_note():
    now = datetime.datetime.now()
    try:
        document = {
            "Signature": {
                "Filename": "Signature",
                # 256*256 PNG
                "Binary": Binary(request.files["signature"].read()),
                "MIME-Type": "image/png"
            },
            "Name": {
                "Filename": "Name",
                "Binary": Binary(request.files["name"].read()),  # ? * ? PNG
                "MIME-Type": "image/png"
            },
            "AddTime": f"{now.year}{now.month}{now.day}"
        }
        signatures.insert_one(document)
    except Exception as e:  # Need to find exceptions TODO
        logging.error(
            f"{e} went wrong on /api/add_note when parsing {request.form}")
        abort(400)
    logging.info("Looks like /api/add_note processed normally")
    return Response(status=201)

@app.route('/<date>')
def main_page(date):
    now = datetime.datetime.now()
    date = date or f"{now.year}{now.month}{now.day}"
    to_render = list()
    for entity in signatures.find({"AddTime":date}):
        to_render.append(entity)
    return render_template("main_page_template.html", documents = to_render)

@app.route('/get_render/<fileId>')
def return_render(fileId):
    logging.info(f"Got a /api/get_render/{fileId}/ request")
    try:
        query = {"_id": ObjectId(fileId)}
        post = signatures.find_one(query)
        return render_template("agreement_template.html", document=post)
    except Exception as e:
        return jsonify({"error": e})


@app.route('/download/signature/<fileId>')
def download_signature(fileId):
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


@app.route('/download/name/<fileId>')
def download_name(fileId):
    try:
        query = {'_id': ObjectId(fileId)}
        doc = signatures.find_one(query)
        fileName = doc["Name"]["Filename"]
        response = make_response(doc["Name"]['Binary'])
        response.headers['Content-Type'] = doc["Name"]["MIME-Type"]
        response.headers["Content-Dispostion"] = "attachment; filename=\"%s\"" % fileName
        return response
    except Exception as e:
        return jsonify({"error": e})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port='80')
