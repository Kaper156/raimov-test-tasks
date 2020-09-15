import pandas as pd
from flask import Flask, request, render_template, json

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/eval_data', methods=['POST'])
def eval_data():
    # Get as json
    json_data = json.loads(request.data)

    dt_range = json_data['rangeStart'], json_data['rangeEnd']
    # Dict for dataframes
    data_frames = dict()
    for name, df in json_data['df'].items():
        # Make df from values
        data_frames[name] = pd.DataFrame(df['values'], index=df['index'])
        # Filter df by datetime range
        data_frames[name] = data_frames[name].loc[dt_range[0]: dt_range[1]]

    # Dict for graphs
    graphs = json_data['graphs']
    for graph in graphs:
        # Eval with graphs with user choice data-frames
        graph['result'] = eval(graph['formula'], {'__builtins__': {}}, data_frames)

        # Convert them into simple python dict to put back
        graph['result'] = graph['result'].to_dict()
        # Bad trick to remove '0':
        graph['result'] = graph['result'][0]

    return json.dumps(graphs)

    # print(request.form)
    # ctx = {
    #     'expressions_ctx': {request.form['expressions']: {'result': '', 'error': ''}, },
    #     'rangeStart': request.form['rangeStart'],
    #     'rangeEnd': request.form['rangeEnd'],
    #
    #
    #     # {expr: {'result': '', 'error': ''} for expr in request.form['graph-formula']},
    # }
    #
    # for expr, expr_ctx in ctx['expressions_ctx'].items():
    #     try:
    #         expr_ctx['result'] = eval(expr, {'__builtins__': {}})
    #     except (NameError, KeyError) as exc:
    #         app.logger.error(exc)
    #         expr_ctx['error'] += f"Cannot access object in expression."
    #     except ZeroDivisionError as exc:
    #         app.logger.error(exc)
    #         expr_ctx['error'] += f"Zero division is not allowed."
    #     except Exception as other_exc:
    #         app.logger.error(other_exc)
    #         expr_ctx['error'] += f"Something went wrong during eval your expression."
    #     finally:
    #         expr_ctx['error'] = f"Error in your expression: {expr}<br>" + expr_ctx['error'] if expr_ctx['error'] else ''
    # return json.dumps(ctx)


if __name__ == '__main__':
    app.run(debug=True)
