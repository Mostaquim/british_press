import json
from django.shortcuts import render, HttpResponse, Http404
from django.middleware.csrf import get_token
from .helpers import place_order, register_user
from .models import CartItems
from formpage.models import CatalogPage
from django.contrib.auth.decorators import login_required


# Create your views here.

# oldTODO create signup and login system
# @ recieve post request from signup
# @ recieve post request from sigin in


def login_signup(request):
    if request.method == 'POST':
        if 'mode' in request.POST:
            if request.POST['mode'] == 'signin':
                print('signin')
                print(request.POST)

            elif request.POST['mode'] == 'register':
                register_user(request)
            else:
                print('u')
                print(request.POST)

    context = {

    }

    return render(request, template_name='clients/confirm_order.html', context=context)



# oldTODO FINE make sure the cart page is complete


def cart_page(request):
    cart = []
    if request.CART:
        cart = request.CART

    items = CartItems.objects.filter(pk__in=cart)

    item_array = []

    if not items.exists():
        c = CatalogPage.objects.all()
        return render(request, template_name='clients/no_item_cart.html', context={'formpages': c})

    total_price_net = 0
    total_price_gross = 0
    total_shipping_net = 0
    total_shipping_gross = 0

    total_net = 0
    total_gross = 0

    for item in items:
        page = CatalogPage.objects.filter(slug=item.slug)
        if page.exists():
            page = page[0]
            item_array.append({
                'detail': json.loads(item.data_name),
                'item': item,
                'page': page
            })

            total_price_net += item.price_net
            total_price_gross += item.price_gross
            total_shipping_net += item.shipping_net
            total_shipping_gross += item.shipping_gross
            total_net += item.price_net + item.shipping_net
            total_gross += item.price_gross + item.shipping_gross
        else:
            item.delete()

    context = {
        'items': item_array,
        'csrf': get_token(request),
        'total_price_net': total_price_net,
        'total_price_gross': total_price_gross,
        'total_shipping_net': total_shipping_net,
        'total_shipping_gross': total_shipping_gross,
        'total_net': total_net,
        'total_gross': total_gross,
    }

    return render(request, template_name='clients/cart_page.html', context=context)


# oldTODO FINE create upload request

def upload_view(request, item_id):
    if request.CART:
        c = CartItems.objects.filter(pk=item_id)
        if c.exists():
            c = c[0]
            if c in request.CART:
                context = {
                    'item': c,
                    'csrf': get_token(request),
                }

                return render(
                    request,
                    template_name='clients/uploadpage.html',
                    context=context
                )

    return HttpResponse(item_id)
