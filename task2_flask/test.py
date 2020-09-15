from unittest import TestCase
from flask import json

from task2_flask.app import app


class EvalDataTestCase(TestCase):
    def test_eval_data(self):
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
            1230,
            1120,
            780,
            1110,
            1110,
            950,
        )
        response = app.test_client().post('/eval_data', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        print(data)
        actual_values = tuple(data[0]['result'].values())

        self.assertEqual(expected_values, actual_values)
