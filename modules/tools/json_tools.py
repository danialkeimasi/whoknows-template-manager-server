import json
from bson import json_util


def to_shell_mode(data_dict):
    return json_util.loads(json.dumps(data_dict))


def to_extended(data_dict):
    return json.loads(json_util.dumps(data_dict))

