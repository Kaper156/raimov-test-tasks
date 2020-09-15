from json import JSONDecodeError

from flask import Flask, request, render_template, json

from task2_flask.logic import eval_graphs

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/eval_data', methods=['POST'])
def eval_data():
    try:
        # Try to get request data as json
        json_data = json.loads(request.data)
    except JSONDecodeError as exc:
        app.logger.error(exc)
        return json.dumps({'error': "Error while parsing json data."})
    graphs = eval_graphs(json_data, app)
    return json.dumps(graphs)


if __name__ == '__main__':
    app.run(debug=True)
