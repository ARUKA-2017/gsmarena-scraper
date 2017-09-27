from flask import Flask, request, Response
from flask_restful import Resource, Api
from json import dumps
import json
from search import getPhoneDetails
from bson import ObjectId

app = Flask(__name__)
api = Api(app)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class getPhone(Resource):
    def get(self, phone):
         data = getPhoneDetails(phone)
         if data != {}:
             
             return {"data":JSONEncoder().encode(data)}
         else:
             return Response("{ 'code': 404, 'message': 'Not Found' }", status=404, mimetype='application/json')


 
api.add_resource(getPhone, '/phone/<string:phone>')


if __name__ == '__main__':
     app.run(host="0.0.0.0")


