from flask import Flask, jsonify, request, make_response, abort
from playhouse.shortcuts import model_to_dict
from renderer import renderpdf
import logging
from models import SignedDocument, db

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
def add_note():
    logging.info("Got a /api/add_note POST request with json {}".format(request.json))
    try:
        document = SignedDocument(
            Place=request.json["Place"],
            DeviceId=request.json['IdDevice'],
            FirstName=request.json['person']['firstName'],
            MiddleName=request.json['person']['middleName'],
            LastName=request.json['person']['lastName'],
            Signature=request.json['person']['signature']
        )
        document.save()
    except:  # Need to find exceptions TODO
        logging.error("Something went wrong on /api/add_note when parsing {}".format(request.json))
        abort(400)
    logging.info("Looks like /api/add_note processed normally")
    return 201


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
        return jsonify({"rendered_document": "rendered_docs/{}.pdf".format(request.json["Id"])}, 200)
    except:  # Need to find exceptions TODO
        logging.error("Something went wrong on /api/get_render when parsing {}".format(request.json))
        abort(400)


@app.route('/api/get_post', methods=['GET'])
def return_post():
    logging.info("Got a /api/get_post GET request")
    try:
        document = SignedDocument.select().where(DeviceId=request.json["Id"]).get()
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


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port='8080')
