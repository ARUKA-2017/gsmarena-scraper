from flask import Flask, request, Response
from flask_restful import Resource, Api
from json import dumps
from search import getPhoneDetails


app = Flask(__name__)
api = Api(app)

class getPhone(Resource):
    def get(self, phone):
         data = getPhoneDetails(phone)
         if data != {}:
             return {"data":data}
         else:
             return Response("{ 'code': 404, 'message': 'Not Found' }", status=404, mimetype='application/json')


 
api.add_resource(getPhone, '/phone/<string:phone>')


if __name__ == '__main__':
     app.run(host="0.0.0.0")