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
    return flask.json.jsonify(get_points(datetime.datetime.fromtimestamp(int(flask.request.form['from'])),
                                         datetime.datetime.fromtimestamp(int(flask.request.form['until'])),
                                         flask.request.form.getlist('target'),
                                         int(flask.request.form['maxDataPoints']),
                                         ))


def get_metrics():
    return [
        {'is_leaf': 1, 'name': 'foo', 'path': 'foo.'},
        {'is_leaf': 1, 'name': 'bar', 'path': 'foo.'},
        {'is_leaf': 0, 'name': 'foo', 'path': ''},
    ]


def connect():
    return psycopg2.connect(os.environ['DATABASE'])


def get_points(from_, until, targets, max_data_points):
    return [{'target': target, 'datapoints': get_db_points(from_, until, target)} for target in targets]


def get_db_points(from_, until, target):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('select value, extract(epoch from timestamp) from points where series = %s', (target,))
    return cursor.fetchall()
