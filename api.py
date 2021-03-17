import sys
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_restful import Resource
from flask_restful import Api, Resource

from tool import ClubhouseUtil, AuthException

app = Flask(__name__)
api = Api(app)


def output_json(data, ok=True):
    return jsonify({"ok": ok, "data": data})


class ClubHouseValidate(Resource):
    def post(self):
        usernames = request.get_json()
        try:
            clubtool = ClubhouseUtil()
            return output_json(clubtool.check_members(usernames))
        except AuthException as e:
            return output_json(e.message, ok=False)
        except Exception as e:
            return output_json(str(e), ok=False)



api.add_resource(ClubHouseValidate, "/validate")


if __name__ == "__main__":
    app.run(debug=True)
