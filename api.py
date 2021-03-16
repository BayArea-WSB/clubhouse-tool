import sys
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_restful import Resource
from flask_restful import reqparse, Api, Resource

from tool import ClubhouseUtil, AuthException

parser = reqparse.RequestParser()

class MyFlaskApp(Flask):
    def run(self, **options):
        if not clubtool.authenticated():
            print(
                "Please config CLUBHOUSE_USER_ID CLUBHOUSE_USER_TOKEN CLUBHOUSE_USER_DEVICE firstly!"
            )
            sys.exit(1)
        super(MyFlaskApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

app = MyFlaskApp(__name__)
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


api.add_resource(ClubHouseValidate, "/validate")


if __name__ == "__main__":
    app.run(debug=True)
