import json
import csv


def inject(data, key, target, target_key):
    _target = target

    if type(target) == dict:
        _target = [target]

    for item in _target:
        if key in item:
            value = next(data_item
                         for data_item in data
                         if data_item['id'] == item[key])
            item.update({target_key: value})
            item.pop(key)
    return _target if type(target) == list else _target[0]


def to_csv(data):
    with open('data.csv', 'w+') as csv_file:
        writer = csv.writer(csv_file)
        write_header = True
        item_keys = []

        for item in data:
            item_values = []
            for key in item:
                if write_header:
                    item_keys.append(key)
                value = item.get(key, '')
                item_values.append(value)
            if write_header:
                writer.writerow(item_keys)
                write_header = False
            writer.writerow(item_values)
