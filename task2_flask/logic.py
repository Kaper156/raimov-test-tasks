import pandas as pd


def eval_graphs(json_data, app):
    try:
        dt_range = json_data['rangeStart'], json_data['rangeEnd']
    except KeyError as exc:
        app.logger.error(exc)
        return {"error": "Wrong JSON-schema"}

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
        try:
            # Eval with graphs with user choice data-frames
            graph['result'] = eval(graph['formula'], {'__builtins__': {}}, data_frames)
        except (NameError, KeyError) as exc:
            app.logger.error(exc)
            graph['error'] = f"Cannot access object in expression."
        except SyntaxError as exc:
            app.logger.error(exc)
            graph['error'] = f"Syntax error in expression."
        except Exception as other_exc:
            app.logger.error(other_exc)
            graph['error'] = f"Something went wrong during eval your expression."
        else:
            # Convert them into simple python dict to put back
            graph['result'] = graph['result'].to_dict()
            # Bad trick to remove '0':
            graph['result'] = graph['result'][0]
    return {"graphs": graphs}
