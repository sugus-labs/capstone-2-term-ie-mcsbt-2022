# Importing required modules
from flask import Flask, jsonify, current_app, request
from sqlalchemy import create_engine
from flask_restx import Api, Namespace, Resource

user = ""
passw = ""
host = ""
database = ""

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = host

# Creating the api V1
api = Api(app, version = '1.0',
    title = 'BEERS API',
    description = """
        API endpoints used to communicate BEERS
        between MySQL database and streamlit
        """,
    contact = "",
    endpoint = "/api/v1"
)

def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
    conn = db.connect()
    return conn

def disconnect(conn):
    conn.close()

beers = Namespace(
    'beers',
    description = 'All the beerrs',
    path='/api/v1')
api.add_namespace(beers)

@beers.route("/beers")
class get_all_beers(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM beer
            LIMIT 10;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@beers.route("/beers/<string:id>")
@beers.doc(params = {'id': 'The ID of the beer'})
class select_user(Resource):

    @api.response(404, "BEER not found")
    def get(self, id):
        id = str(id)
        conn = connect()
        select = """
            SELECT *
            FROM beer
            WHERE id = '{0}';""".format(id)
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@beers.route("/breweries")
class get_all_beers(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM brewery
            LIMIT 10;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@beers.route("/breweries/<string:id>")
@beers.doc(params = {'id': 'The ID of the brewery'})
class select_user(Resource):

    @api.response(404, "BREWERY not found")
    def get(self, id):
        id = str(id)
        conn = connect()
        select = """
            SELECT *
            FROM brewery
            WHERE id = '{0}';""".format(id)
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0', 
        port = 8080,
        debug = True)