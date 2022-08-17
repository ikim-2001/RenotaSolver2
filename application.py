from flask import Flask, request, jsonify, make_response

import json_inequalities
from main import *
from json_inequalities import dict
from flask_cors import CORS

application = Flask(__name__)
CORS(application)

@application.route("/test", methods=["GET", "POST"])
def test():
    if request.method == "GET":
        return jsonify({"response": "Get Request Called"})
    elif request.method == "POST":
        req_json = request.get_json()
        instance = Main(req_json["mathpix-output"])
        response = instance.main()
        return jsonify(response)

if __name__ == "__main__":
    application.run(debug=True, port=9090)