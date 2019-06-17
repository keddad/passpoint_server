from flask import Flask, jsonify, request, make_response, abort, Response
from playhouse.shortcuts import model_to_dict
from renderer import renderpdf
import logging
from models import SignedDocument, db
from datetime import date

logging.basicConfig(filename="log",
                    format='%(asctime)-6s: %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s',
                    level=logging.DEBUG)

app = Flask(__name__)

db.connect()
db.create_tables([SignedDocument])


@app.errorhandler(400)
def bad_request():
    return make_response((jsonify({'error': 'Bad request'}), 400))


@app.errorhandler(404)
def bad_request():
    return make_response((jsonify({'error': 'Bad route'}), 404))


@app.route('/api/add_note', methods=['POST'])
def add_note():d
    try:
        document = SignedDocument(
            Place=request.form["Place"],
            DeviceId=request.form['IdDevice'],
            FirstName=request.form['firstName'],
            MiddleName=request.form['middleName'],
            LastName=request.form['lastName'],
            Signature=request.form['signature']
        )
        document.save()
    except:  # Need to find exceptions TODO
        logging.error("Something went wrong on /api/add_note when parsing {}".format(request.json))
        abort(400)
    logging.info("Looks like /api/add_note processed normally")
    return Response(status=201) 


@app.route('/api/get_render', methods=['GET'])
def return_render():
    logging.info("Got a /api/get_render GET request")
    try:
        document = SignedDocument.select().where(DeviceId=int(request.json["Id"])).get()
        rendered_document = renderpdf(document)
        with open("rendered_docs/{}.pdf".format(request.json["Id"]), 'wb') as file:
            file.write(rendered_document)
            logging.info("New document in rendered_docs/{}.pdf".format(request.json["Id"]))
        logging.info("Looks like /api/get_render processed normally")
        return jsonify({"RenderedDocument": "rendered_docs/{}.pdf".format(request.json["Id"])}, 200)
    except:  # Need to find exceptions TODO
        logging.error("Something went wrong on /api/get_render when parsing {}".format(request.json))
        abort(400)


@app.route('/api/get_post', methods=['GET'])
def return_post():
    logging.info("Got a /api/get_post GET request")
    try:
        document = SignedDocument.select().where(DeviceId=int(request.json["Id"])).get()
        document_data = model_to_dict(document)
        logging.info("Looks like /api/get_post processed normally")
        return jsonify(document_data), 200
    except:
        logging.error("Something went wrong on /api/get_post when parsing {}".format(request.json))
        abort(400)


@app.route("/api/get_latest", methods=['GET'])
def return_latest():
    offset = 1
    to_return = []
    try:
        offset = request.json['offset']
    except:  # Need to find exceptions TODO
        abort(400)
    for doc in SignedDocument.select().order_by(SignedDocument.SignedDate):
        to_return.append(model_to_dict(doc))
        offset -= 1
        if not offset:
            break
    return jsonify(to_return), 200


@app.route("/api/return_query", methods=['GET'])
def return_query():
    try:
        tmp = []
        req = request.json
        if "Older" in req:
            req["Older"] = date.fromtimestamp(req["Older"])
        if "Newer" in req:
            req["Newer"] = date.fromtimestamp(req["Newer"])
        for key, value in req['arguments'].items():
            sunion = set()
            for doc in SignedDocument.select().where(key == value).order_by(SignedDocument.SignedDate):
                sunion += doc
            tmp += sunion
        out_set = set()
        out_set = tmp[0].union(*tmp[1:])
        return(jsonify(out_set), 200)
    except:
        abort(400)






if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port='8080')
