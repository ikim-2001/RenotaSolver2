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
        req_json = request.json
        instance = Main(req_json["mathpix-output"])
        print(instance.main())
        return jsonify(instance.main())

    # req_Json = request.json
    # print(req_Json)
    # json_inequalities.dict = req_Json["mathpix-output"]
    # # json_inequalities.print_dict(json_inequalities.dict)
    # instance = Main(req_Json["mathpix-output"])
    # # response is now a valid json object
    # response = jsonify(instance.main())
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # return response



if __name__ == "__main__":
    application.run(debug=True, port=9090)