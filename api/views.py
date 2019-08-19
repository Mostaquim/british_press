import json
import hashlib
import os
import uuid
from django.shortcuts import render, HttpResponse, Http404
from django.conf import settings
from requests import Session
from .client import SoapClient
from clients.models import UploadedFile
from zeep.helpers import serialize_object
from .helper import (
    create_item_id,
    handle_uploaded_file,
    get_total_price,
    get_selected
)

from clients.models import CartItems, UploadedFile
from .decorator import json_response_cache_page_decorator

from django.core.cache import cache

from django.utils.encoding import force_bytes, iri_to_uri

from django.contrib.sessions.backends.db import SessionStore

from random import randint

from ordercart.models import Address, OrderGroup


def catalog_api(request):
    if request.is_ajax():
        if request.method == 'POST':
            # CREATE THE CACHE KEY
            cache_key = 'json_response_cache:{}'.format(
                hashlib.md5(request.body).hexdigest()
            )
            print(cache_key)

            content = cache.get(cache_key)

            if content is not None:
                return HttpResponse(
                    content,
                    content_type='application/json'
                )

            data = request.body

            data = json.loads(request.body.decode('utf-8'))
            if 'selected' in data:
                selected = {
                    'optionIds': [],
                    'shippingDestinationChoice': 0,
                }

                for key, val in data['selected'].items():
                    selected['optionIds'].append({
                        'name': key,
                        'value': val
                    })

        client = SoapClient().get_catalog_client()

        with client.settings(strict=False):
            response = client.service.getCustomCatalogue(
                environment=settings.ENVIRONMENT,
                selected=selected,
                messageLevel='all'
            )

        if response.response.responseCode:

            content = json.dumps(
                get_selected(
                    serialize_object(response.productList)
                )
            )
            cache.set(cache_key, content, settings.API_CACHE_TIME)
            return HttpResponse(content, content_type="application/json")


def add_to_cart(request):
    if request.is_ajax():
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            if 'selected' in data:
                cart_item = CartItems(
                    slug=data['slug'],
                    data_vals=json.dumps(data['selected']),
                    data_name=json.dumps(data['selected_names']),
                    price_net=data['prices']['priceNet'],
                    price_gross=data['prices']['priceGross'],
                    shipping_net=data['prices']['shippingNet'],
                    shipping_gross=data['prices']['shippingGross'],
                )

                cart_item.save()

                if request.user.is_authenticated:
                    cart_item.user = request.user
                    cart_item.save()

                if request.session:
                    s = request.session
                else:
                    s = SessionStore()

                if 'cart' in s:
                    s['cart'].append(cart_item.pk)
                else:
                    s['cart'] = [cart_item.pk]

                s.save()

                new_item = {
                    'data_name': json.loads(cart_item.data_name),
                    'price': {
                        'price_gross': cart_item.price_gross,
                        'price_net': cart_item.price_net,
                        'shipping_gross': cart_item.shipping_gross,
                        'shipping_net': cart_item.shipping_net,
                    }
                }

                items = CartItems.objects.filter(pk__in=s['cart'])

                total_price = get_total_price(items)

                response_json = {
                    'new_item': new_item,
                    'total_price': total_price,
                    'count': items.count()
                }

                response = json.dumps(response_json)

                return HttpResponse(response, content_type="application/json")


def file_upload(request):
    if request.method == 'POST':
        f = request.FILES['file']
        fname = handle_uploaded_file(f)
        return HttpResponse(fname)
    raise Http404()


def remove_item_from_cart(request):
    # Create api for recieving remove request
    # @ recieve item object in post request
    # @ find cart item in CartItems Model and delete it
    # @ return a success message if it's deleted

    if request.is_ajax():
        if request.method == 'POST':
            item = request.POST['item']
            c = CartItems.objects.filter(pk=item)
            if c.exists():
                c = c[0]
                if not c in request.CART:
                    return HttpResponse('OK')
                else:
                    c.delete()
                    return HttpResponse('ok')
    raise Http404()


def upload_design(request):
    """
    FINE create upload design request
    @ create separate file modal and save it there
    @ check if file with same name exists in the modal
    @ find if the session has the related cart item
    @ return proper response
    """

    response = {
        'status': 'failed',
        'message': 'unauthorized access'
    }

    if request.is_ajax() \
            and request.method == 'POST' \
            and 'item' in request.POST \
            and request.CART:

        item_id = request.POST['item']
        c = CartItems.objects.filter(pk=item_id)

        if c.exists() and c[0] in request.CART:
            c = c[0]
            f = request.FILES['formData']
            ext = ''
            if '.' in f.name:
                ext = f.name.split('.')[1]

            uploaded_file = UploadedFile(
                name=f.name,
                saved_name=f.name,
                cart_item=c,
                file_type=ext
            )

            tmp_path = os.path.join(settings.UPLOAD_DIR, str(c.pk))
            if not os.path.exists(tmp_path):
                os.makedirs(tmp_path)

            main_path = os.path.join(tmp_path, f.name)
            i = 0
            while os.path.exists(main_path):
                tmp_name = f.name
                if i:
                    tmp_name = str(i) + '_' + f.name
                main_path = os.path.join(tmp_path, tmp_name)
                i += 1

            with open(main_path, 'wb+') as dest:
                for chunk in f.chunks():
                    dest.write(chunk)

            uploaded_file.saved_path = main_path

            uploaded_file.save()

            response = {
                'status': 'OK',
                'file_name': uploaded_file.name,
                'file_id': uploaded_file.pk
            }

        else:
            response = {
                'status': 'ERR',
                'message': 'Invalid Session'
            }

    return HttpResponse(json.dumps(response), content_type="application/json")


# recieve backend

def delete_file(request):
    if request.is_ajax() and \
        'cart' in request.session \
            and request.method == 'POST':
        if 'item_id' in request.POST and 'file_id' in request.POST:
            item_id = request.POST['item_id']
            file_id = request.POST['file_id']
            if int(item_id) in request.session['cart']:
                item = CartItems.objects.filter(pk=item_id)
                if item.exists():
                    item = item[0]
                    f = UploadedFile.objects.filter(pk=file_id)
                    if f.exists():
                        f = f[0]
                    if f in item.files.all():
                        f.delete()
                        return HttpResponse('OK')

    return HttpResponse('failed')


def create_address(request):
    # oldTODO create address in modal
    # @ create address from post request

    if request.is_ajax() \
            and request.user.is_authenticated \
            and request.method == 'POST':

        p = request.POST

        adr = Address(
            company=p['company'],
            street=p['street'],
            houseNumber=p['house_number'],
            phonePrefix=p['phonePrefix'],
            phoneNumber=p['phoneNumber'],
            zipcode=p['zip_code'],
            city=p['city'],
            user=request.user,
        )
        adr.save()

        response = {
            'adr_id': adr.pk,
            'adr_name': '%s, %s, %s' % (adr.street, adr.houseNumber, adr.zipcode),
            'STATUS': 'OK'
        }

        return HttpResponse(json.dumps(response), content_type='application/json')
    raise Http404()


# backend for address selection

def select_address(request):
    if request.is_ajax() \
            and request.user.is_authenticated \
            and request.method == 'POST':
        address_id = request.POST['id']
        adr = Address.objects.filter(pk=address_id)
        if adr.exists() and adr[0].user == request.user:
            adr = adr[0]
            order_group = OrderGroup.objects.filter(user=request.user)
            if order_group.exists():
                order_group = order_group[0]
                if request.POST['type'] == 'delivery':
                    order_group.delivery_address = adr
                else:
                    order_group.billing_address = adr

                order_group.save()
                response = {
                    'street': adr.street,
                    'company': adr.company,
                    'houseNumber': adr.houseNumber,
                    'zipcode': adr.zipcode,
                    'city': adr.city,
                    'phonePrefix': adr.phonePrefix,
                    'phoneNumber': adr.phoneNumber
                }

                return HttpResponse(json.dumps(response), content_type='application/json')
