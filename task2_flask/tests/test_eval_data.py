from copy import deepcopy
from unittest import TestCase
from flask import json

from task2_flask.app import app


class TestSettings:
    data = {
        "rangeEnd": "2020-09-06T00:00:00",
        "rangeStart": "2020-09-02T00:00:00",
        "graphs": [
            {
                "formula": "CPULoad5min*10"
            }
        ],
        "df": {
            "CPULoad5min": {
                "index": [
                    "2020-09-02T00:01:49",
                    "2020-09-02T00:06:37",
                    "2020-09-02T00:11:36",
                    "2020-09-02T00:16:54",
                    "2020-09-02T00:21:35",
                    "2020-09-02T00:26:32"
                ],
                "values": [
                    123,
                    112,
                    78,
                    111,
                    111,
                    95
                ]
            }
        }
    }
    expected_values = (
        123,
        112,
        78,
        111,
        111,
        95,
    )
    url = '/eval_data'

    @staticmethod
    def make_response(data):
        return app.test_client().post(TestSettings.url, data=json.dumps(data), content_type='application/json')

    @staticmethod
    def resp_to_json(response):
        return json.loads(response.data)

    @staticmethod
    def catch_values(response):
        return tuple(TestSettings.resp_to_json(response)['graphs'][0]['result'].values())


class EvalDataSimplestTestCase(TestCase):

    def setUp(self) -> None:
        self.data = deepcopy(TestSettings.data)
        self.expected_values = TestSettings.expected_values
        self.make_response = TestSettings.make_response
        self.url = TestSettings.url
        self.resp_to_json = TestSettings.resp_to_json
        self.catch_values = TestSettings.catch_values

    # Simplest tests
    def test_eval_data(self):
        # Multiply values by 10
        self.expected_values = tuple(map(lambda x: x * 10, self.expected_values))

        response = self.make_response(self.data)
        self.assertEqual(200, response.status_code)

        actual_values = self.catch_values(response)
        self.assertEqual(actual_values, self.expected_values)

    def test_eval_data_graph_is_graph(self):
        # Modify formula
        self.data['graphs'][0]['formula'] = "CPULoad5min"

        response = self.make_response(self.data)
        self.assertEqual(200, response.status_code)

        actual_values = self.catch_values(response)
        self.assertEqual(actual_values, self.expected_values)

    def test_eval_data_graph_multiple_one_is_graph(self):
        # Modify formula
        self.data['graphs'][0]['formula'] = "CPULoad5min*1"

        response = self.make_response(self.data)
        self.assertEqual(response.status_code, 200)

        actual_values = self.catch_values(response)
        self.assertEqual(self.expected_values, actual_values)


class EvalDataIncorrectDataTestCase(TestCase):

    def setUp(self) -> None:
        self.data = deepcopy(TestSettings.data)
        self.expected_values = TestSettings.expected_values
        self.make_response = TestSettings.make_response
        self.url = TestSettings.url
        self.resp_to_json = TestSettings.resp_to_json
        self.catch_values = TestSettings.catch_values
    # Check errors tests
    def test_eval_data_incorrect_json(self):
        incorrect_json_string = "{ [ }"
        response = app.test_client().post(
            self.url, data=incorrect_json_string, content_type='application/json'
        )
        self.assertEqual(200, response.status_code)

        data = self.resp_to_json(response)
        self.assertIn('error', data)
        self.assertIn("Error while parsing json data.", data['error'])

    def test_eval_data_incorrect_formula(self):
        self.data['graphs'][0]['formula'] = "CPULoad5min*NOT_EXISTED_DF"

        response = self.make_response(self.data)
        self.assertEqual(200, response.status_code)

        data = self.resp_to_json(response)['graphs'][0]
        self.assertIn('error', data)
        self.assertIn("Cannot access object in expression.", data['error'])

    def test_eval_data_incorrect_syntax(self):
        self.data['graphs'][0]['formula'] = "CPULoad5min*CPULoad5min ) "

        response = self.make_response(self.data)
        self.assertEqual(200, response.status_code)

        data = self.resp_to_json(response)['graphs'][0]
        self.assertIn('error', data)
        self.assertIn("Syntax error in expression.", data['error'])


class EvalDataManyDFManyFormulasTestCase(TestCase):
    def setUp(self) -> None:
        self.data = deepcopy(TestSettings.data)
        self.data['df']["CPULoad1min"] = {
            "index": [
                "2020-09-03T00:01:49",
                "2020-09-03T00:06:37",
                "2020-09-03T00:11:36",
                "2020-09-03T00:16:54",
                "2020-09-03T00:21:35",
                "2020-09-03T00:26:32"
            ],
            "values": list(range(-3, 3, 1))
        }
        # Add simple operations between two DF
        self.data['graphs'] += [{"formula": f"CPULoad5min {op} CPULoad1min"} for op in ['+', '-', '/', '*', '**']]

        self.make_response = TestSettings.make_response
        self.resp_to_json = TestSettings.resp_to_json

    def test_eval_data(self):
        response = self.make_response(self.data)
        self.assertEqual(200, response.status_code)

        data = self.resp_to_json(response)
        self.assertNotIn('error', data)
        self.assertIn('graphs', data)
        for graph in data['graphs']:
            self.assertNotIn('error', graph, msg=f"(expression: '{graph['formula']}')")


class EvalDataWrongSchemaTestCase(TestCase):
    def setUp(self) -> None:
        self.data = deepcopy(TestSettings.data)
        self.url = TestSettings.url

        self.make_response = TestSettings.make_response
        self.resp_to_json = TestSettings.resp_to_json

    def test_eval_data_wrong_range_key_start(self):
        self.data['start-of-the-range'] = self.data["rangeStart"]
        del self.data["rangeStart"]

        response = self.make_response(self.data)
        self.assertIs(200, response.status_code)

        data = self.resp_to_json(response)
        self.assertIn('error', data)
        self.assertIn("Wrong JSON-schema", data['error'])

    def test_eval_data_wrong_range_key_end(self):
        self.data['end-of-the-range'] = self.data["rangeEnd"]
        del self.data["rangeEnd"]

        response = self.make_response(self.data)
        self.assertIs(200, response.status_code)

        data = self.resp_to_json(response)
        self.assertIn('error', data)
        self.assertIn("Wrong JSON-schema", data['error'])

