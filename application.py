from flask import Flask, request, jsonify

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
        instance = Main(req_json.get("mathpix-output"))
        response = instance.main()
        print(response)
        return jsonify(response)

if __name__ == "__main__":
    application.run(debug=True, port=9090)