import json
import hashlib
from django.shortcuts import render, HttpResponse, Http404
from django.conf import settings
from requests import Session
from .client import SoapClient
from zeep.helpers import serialize_object
from .helper import create_item_id, handle_uploaded_file
from clients.models import Orders
from .decorator import json_response_cache_page_decorator

from django.core.cache import cache

from django.utils.encoding import force_bytes, iri_to_uri

from django.contrib.sessions.backends.db import SessionStore


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
            content = json.dumps(serialize_object(response.productList))
            cache.set(cache_key, content, settings.API_CACHE_TIME)
            return HttpResponse(content, content_type="application/json")


def create_product(request):
    if request.is_ajax():
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            if 'formData' in data and 'selected' in data:
                client = SoapClient().get_catalog_client()

                item_identifier = create_item_id(data['formData'])

                selected = {
                    'optionIds': [],
                    'shippingDestinationChoice': 0,
                    'itemIdentifier': item_identifier
                }

                for key, val in data['selected'].items():
                    selected['optionIds'].append({
                        'name': key,
                        'value': val
                    })

                with client.settings(strict=False):
                    response = client.service.setCustomProduct(
                        environment=settings.ENVIRONMENT,
                        product=selected,
                        writeMode='save',
                        messageLevel='all'
                    )

                    if response.response.responseCode:
                        formData = data['formData']
                        order = Orders.objects.create_new_order(
                            email=formData['email'],
                            first_name=formData['firstName'],
                            last_name=formData['lastName'],
                            salutation=formData['salutation'],
                            street=formData['street'],
                            house_number=formData['houseNumber'],
                            zip_code=formData['zipCode'],
                            city=formData['city'],
                            phone_number=formData['phoneNumber'],
                            phone_prefix=formData['phonePrefix'],
                            item_id=item_identifier,
                            comment=formData['comment'],
                            company=formData['company']
                        )

                        order.save()

                        order.data = json.dumps(data['selected']) 
                        order.save()

                        return HttpResponse(order.id)
                    else:
                        return HttpResponse('0')
    raise Http404()


def file_upload(request):
    if request.method == 'POST':
        f = request.FILES['file']
        fname = handle_uploaded_file(f)

        return HttpResponse(fname)
    raise Http404()


def create_session(request):
    s = SessionStore()
    s['a'] = 'test'
    
    print(s.session_key)
    return HttpResponse(s)
