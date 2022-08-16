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
        json_inequalities.dict = req_Json["mathpix-output"]
        json_inequalities.print_dict(json_inequalities.dict)
        instance = Main(req_Json["mathpix-output"])
        return instance.main()



if __name__ == "__main__":
    application.run(debug=True, port=9090)