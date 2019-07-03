from flask import Flask, jsonify, request, make_response, abort, Response, render_template
import logging
import os
import bson
from bson.binary import Binary
from bson.objectid import ObjectId
import datetime
from pymongo import MongoClient



client = MongoClient("localhost", 27017)
signatures = client.db.signatures  # collecrion used to store all the stuff

logging.basicConfig(filename="passpoint_server.log",
                    format='%(asctime)-6s: %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s',
                    level=logging.DEBUG)  # come logging features

app = Flask(__name__)


@app.route('/add_note', methods=['POST'])
def add_note():
    logging.info(f"Got a /add_note/ request")
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
                "Binary": Binary(request.files["name"].read()),  # 1054*110 PNG
                # hardcoded data is AMAZING! I love it.
                "MIME-Type": "image/png"
            },
            # date used to perform search queries
            "LookupTime": f"{now.year}{now.month}{now.day}",
            # actually a feature
            "VisualTime": f"{now.year}.{now.month}.{now.day}"
        }
        signatures.insert_one(document)
    except Exception as e:  # Need to find exceptions TODO
        logging.error(
            f"{e} went wrong on /add_note when parsing {request.form}")
        abort(400)
    logging.info("Looks like /add_note processed normally")
    return Response(status=201)


@app.route('/<date>')
def main_page(date):
    logging.info(f"Got a / request")
    now = datetime.datetime.now()
    date = date or f"{now.year}{now.month}{now.day}"
    to_render = list()
    for entity in signatures.find({"LookupTime": date}): # Find all the signatures from requred date
        to_render.append(entity)
    return render_template("main_page_template.html", documents=to_render)


@app.route('/get_render/<fileId>') # Request to get rendered page
def return_render(fileId):
    logging.info(f"Got a /get_render/{fileId}/ request")
    try:
        query = {"_id": ObjectId(fileId)}
        post = signatures.find_one(query)
        return render_template("agreement_template.html", document=post)
    except Exception as e:
        return jsonify({"error": e})


@app.route('/download/signature/<fileId>') # Request to download a signature file
def download_signature(fileId):
    logging.info(f"Got a /download/signature/{fileId}/ request")
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


@app.route('/download/name/<fileId>') # Request to download a "name" file, signature description
def download_name(fileId):
    try:
        logging.info(f"Got a /download/name/{fileId}/ request")
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
