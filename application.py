from flask import Flask, request, jsonify

import json_inequalities
from main import *
from json_inequalities import dict


application = Flask(__name__)

@application.route("/test", methods=["GET", "POST"])
def test():
    if request.method == "GET":
        return jsonify({"response": "Get Request Called"})
    elif request.method == "POST":
        req_Json = request.json
        instance = Main(req_Json["mathpix-output"])
        # response is now a valid json object
        response = jsonify(instance.main())
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response




if __name__ == "__main__":
    application.run(debug=True, port=9090)