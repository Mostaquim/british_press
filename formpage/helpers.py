import json


def get_product_name(d):
    d = json.loads(d)
    d = d['optionIds']

    for i in d:
        if i['name'] == 'product':
            return i['value']
