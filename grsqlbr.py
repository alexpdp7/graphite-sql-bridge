import datetime
import flask
import flask_cors
import os
import psycopg2


app = flask.Flask(__name__)
flask_cors.CORS(app)


@app.route('/metrics/find/')
def find():
    return flask.json.jsonify(metrics=get_metrics())


@app.route('/render', methods=['POST'])
def render():
    assert flask.request.form['format'] == 'json'
    return flask.json.jsonify(get_points(flask.request.form.getlist('target'),
                                         int(flask.request.form['maxDataPoints']),
                                         ))


def get_metrics():
    return []


def connect():
    return psycopg2.connect(os.environ['DATABASE'])


def get_points(targets, max_data_points):
    return [{'target': target, 'datapoints': get_db_points(target)} for target in targets]


def get_db_points(target):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('select value, extract(epoch from timestamp) from points where series = %s', (target,))
    return cursor.fetchall()
