import os
import uuid
import json
from django.conf import settings
from clients.models import CartItems
from django.core import serializers


def create_item_id(formData):
    i = 1
    z = True
    while z:
        item_id = "%s_%s_%s" % (formData['firstName'], formData['lastName'], i)
        item_id = item_id.replace(' ', '_')
        o = Orders.objects.filter(item_id=item_id)
        if not o.exists():
            return item_id
        i += 1


def handle_uploaded_file(f):
    ext = f.name.split('.')[1]
    fname = uuid.uuid4().hex + '.' + ext
    main_path = os.path.join(settings.UPLOAD_DIR,  fname)
    with open(main_path, 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
    return fname


def get_total_price(items):
    price_net = 0
    price_gross = 0
    shipping_gross = 0
    shipping_net = 0
    for item in items:
        price_net += item.price_net
        price_gross += item.price_gross
        shipping_gross += item.shipping_gross
        shipping_net += item.shipping_net

    return {
        'price_net': price_net,
        'price_gross': price_gross,
        'shipping_gross': shipping_gross,
        'shipping_net': shipping_net
    }


def get_selected(response):
    select_list = response['selectGroupList']
    selected_option_id = response['selected']['optionIds']
    selected = {}
    for opt in selected_option_id:
        selected[opt['name']] = opt['id']
    i = 0
    for s in select_list:
        optlist = s['optionList']
        s_name = s['selectName']
        j = 0

        for o in optlist:
            response['selectGroupList'][i]['optionList'][j]['selected'] = False
            if selected[s_name] == o['optionId']:
                print(s_name)
                print(o['optionName'])
                response['selectGroupList'][i]['optionList'][j]['selected'] = True
                print(response['selectGroupList'][i]['optionList'][j])
                

            j += 1

        i += 1

    return response
