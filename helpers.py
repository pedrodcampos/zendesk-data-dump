import json
import csv
import os.path as path
from os import makedirs
from collections import OrderedDict


def inject(data, key, target, target_key):
    _target = target

    if type(target) == dict:
        _target = [target]

    for item in _target:
        if key in item:
            if data:
                value = next((data_item
                              for data_item in data
                              if data_item['id'] == item[key]), None)
                item.update({target_key: value})
            else:
                item.update({target_key: None})

            item.pop(key)
    return _target if type(target) == list else _target[0]


def get_flatten_key_value_pairs(data, root=None):
    if isinstance(data, dict):
        for key, value in data.items():
            if root and root == 'custom_fields':
                if key == 'id':
                    yield (data['id'], data['value'])
            elif root:
                path = root+'-'+key
                yield from get_flatten_key_value_pairs(value, path)
            else:
                path = key
                yield from get_flatten_key_value_pairs(value, path)
    elif isinstance(data, list):
        if all(map(lambda x: not isinstance(x, (dict, list)), data)):
            yield (root, ", ".join(map(str, [item for item in data])))
        else:
            for item in data:
                yield from get_flatten_key_value_pairs(item, root)
    else:
        yield (root, data)


def flatten_dict(data):
    flattened = dict(get_flatten_key_value_pairs(data))
    return flattened


def get_unique_keys_from_dict_list(data):
    keys = []
    for item in data:
        for k in item.keys():
            if k not in keys:
                keys.append(k)
    return keys


def to_csv(data, filename):
    target_folder = path.join(path.curdir, 'exports')
    target_full_path = path.join(target_folder, filename)
    makedirs(target_folder, exist_ok=True)
    with open(target_full_path, 'w+', encoding='utf-8-sig', newline="") as csv_file:
        ordered_keys = get_unique_keys_from_dict_list(data)
        writer = csv.DictWriter(csv_file, ordered_keys, dialect='excel')
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    return target_full_path
