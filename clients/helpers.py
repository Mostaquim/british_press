import json
import uuid
from .models import Clients, User, CartItems
from api.client import SoapClient
from django.conf import settings
from django.db import transaction
from django.contrib.auth import login
from django.shortcuts import HttpResponseRedirect


def place_order(order_id, uploaded_file):
    order = Orders.objects.get(pk=order_id)
    order_name = uuid.uuid4().hex

    order_data = order.data

    shipping = 'Default'

    if order_data:
        order_data = json.loads(order_data)
        if 'shipping' in order_data:
            if order_data['shipping'] == 'priority':
                shipping = order_data['shipping'].capitalize()

    orderInformation = {
        'customerProductId': order.item_id,
        'orderQuanitity': 1,
        'shippingType': shipping,
        'orderName': order_name,
        'customerComment': order.comment,
        'customerCopy': 5,
    }

    paymentInformation = {
        'paymentMethod': 'INV'
    }

    shippingInformation = {
        'company': order.client.company,
        'salutation': order.client.salutation,
        'firstName': order.client.user.first_name,
        'lastName': order.client.user.last_name,
        'street': order.client.street,
        'houseNumber': order.client.house_number,
        'zipcode': order.client.zip_code,
        'city': order.client.city,
        'phonePrefix': order.client.phone_prefix,
        'phoneNumber': order.client.phone_number
    }

    dataSourceInformation = {
        'dataSourceHost': settings.BASE_URL + '/uploads/' + uploaded_file
    }

    client = SoapClient().get_order_client()

    validate = 1

    with client.settings(strict=False):
        response = client.service.createOrder(
            environment=settings.ENVIRONMENT,
            accountInformation=settings.ACCOUNT_SETTING,
            orderInformation=orderInformation,
            paymentinformation=paymentInformation,
            shippingInformation=shippingInformation,
            dataSourceInformation=dataSourceInformation,
            validate=validate,
            messageLevel='all'
        )

        return response.response.responseCode


def register_user(request):
    p = request.POST

    email = p['email']
    password = p['password']

    salutation = p['salutation']
    last_name = p['last_name']
    first_name = p['first_name']

    street = p['street']
    house_number = p['house_number']
    zip_code = p['zip_code']
    city = p['city']

    company = p['company']
    phone_prefix = p['phone_prefix']
    phone_number = p['phone_number']

    try:
        with transaction.atomic():
            user = User(
                email=email,
                username=email,
                password=None,
                first_name=first_name,
                last_name=last_name
            )

            user.set_password(None)
            user.save()

            client = Clients(
                user=user,
                company=company,
                salutation=salutation,
                phone_number=phone_number,
                phone_prefix=phone_prefix,
                house_number=house_number,
                zip_code=zip_code,
                city=city,
                street=street
            )

            client.save()

            if 'cart' in request.session:
                cart = request.session['cart']
                items = CartItems.objects.filter(pk__in=cart)

                for item in items:
                    item.user = user
                    item.save()

            login(request, user)

            request.session['cart'] = cart

            print(request.session)

    except Exception as e:
        print(e)
        return 'err'


