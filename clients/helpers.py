import json
import uuid
from .models import Orders, Clients
from api.client import SoapClient
from django.conf import settings


def place_order(order_id, uploaded_file):
    order = Orders.objects.get(pk=order_id)
    order_name= uuid.uuid4().hex

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
        'dataSourceHost' : settings.BASE_URL + '/uploads/' + uploaded_file
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
