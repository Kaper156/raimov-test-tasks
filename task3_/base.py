import json

json_like_string = "{}"
json_like_dict = json.loads(json_like_string)
json_like_string = json.dumps(json_like_dict)
