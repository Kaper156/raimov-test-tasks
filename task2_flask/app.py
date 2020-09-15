from flask import Flask, request, render_template, json

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/eval_data', methods=['POST'])
def eval_data():
    ctx = {'error': '', 'result': ''}
    expression = request.form['expression']
    try:
        ctx['result'] = eval(expression, {'__builtins__': {}})
    except NameError as exc:
        app.logger.error(exc)
        ctx['error'] += f"Cannot access object in expression, check it please: {expression}\n"
    except Exception as other_exc:
        app.logger.error(other_exc)
        ctx['error'] += f"Something went wrong"
    finally:
        return json.dumps(ctx)


if __name__ == '__main__':
    app.run(debug=True)
