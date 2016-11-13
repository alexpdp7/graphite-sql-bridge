import flask
import flask_cors


app = flask.Flask(__name__)
flask_cors.CORS(app)


@app.route('/metrics/find/')
def find():
    return flask.json.jsonify(metrics=get_metrics())


@app.route('/render', methods=['POST'])
def render():
    assert flask.request.form['format'] == 'json'
    return flask.json.jsonify(get_points(flask.request.form['from'],
                                         flask.request.form['until'],
                                         flask.request.form.getlist('target'),
                                         flask.request.form['maxDataPoints'],
                                         ))


def get_metrics():
    return [
        {'is_leaf': 1, 'name': 'foo', 'path': 'foo.'},
        {'is_leaf': 1, 'name': 'bar', 'path': 'foo.'},
        {'is_leaf': 0, 'name': 'foo', 'path': ''},
    ]


def get_points(from_, until, targets, max_data_points):
    return [{'target': target, 'datapoints': random_data_points()} for target in targets]


def random_data_points():
    import datetime
    import random
    return [[random.randint(0,100), int(datetime.datetime.now().timestamp()) - 6000 + i*60] for i in range(0,100)]
