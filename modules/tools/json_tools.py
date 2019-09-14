import json

from bson import json_util
from dict_deep import deep_set

def to_shell_mode(data_dict):
    return json_util.loads(json.dumps(data_dict))


def to_extended(data_dict):
    return json.loads(json_util.dumps(data_dict))


def nested_to_dotted(mixed, key='', dots={}):
    if isinstance(mixed, dict):
        for (k, v) in mixed.items():
            nested_to_dotted(mixed[k], '%s.%s' % (key, k) if key else k)
    else:
        dots[key] = mixed

    return dots


def dotted_to_nested(dotted):
    nested = {}

    for key, value in dotted.items():
        deep_set(nested, key, value, default=lambda: dict())

    return nested
