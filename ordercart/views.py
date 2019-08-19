import json

from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Address, OrderGroup


@login_required(login_url='/login_signup/')
def order_list(request):
    if request.CART:
        c = request.CART
        order_group = OrderGroup.objects.filter(
            user=request.user, order_placed=False)
        if order_group.exists():
            order_group = order_group[0]
        else:
            order_group = OrderGroup(user=request.user)
            order_group.save()

        items = []

        order_group_items = order_group.items.all()

        for item in c:
            if item not in order_group_items:
                order_group.items.add(item)
            data_name = json.loads(item.data_name)
            items.append(
                {
                    'id': item.pk,
                    'price': item.price_net + item.shipping_net,
                    'quantity': data_name['quantity'],
                    'props': data_name
                }
            )

        context = {
            'items': items
        }

        return render(request, template_name="order/list.html", context=context)


@login_required(login_url='/login_signup/')
def delivery_option(request):
    order_group = OrderGroup.objects.filter(
        user=request.user, order_placed=False)

    if order_group.exists():
        order_group = order_group[0]
    else:
        return HttpResponseRedirect('/order/list/')

    context = {
        'delivery_address': order_group.delivery_address,
        'billing_address': order_group.billing_address,
        'addresses': request.user.address.all()
    }

    return render(request, template_name="order/delivery.html", context=context)


@login_required(login_url='/login_signup/')
def review(request):
    order_group = OrderGroup.objects.filter(
        user=request.user, order_placed=False
    )
    if order_group.exists():
        order_group = order_group[0]
    else:
        return HttpResponseRedirect('/order/list/')

    items = []
    total_price = 0
    c = request.CART

    for item in c:
        data_name = json.loads(item.data_name)
        total_price += item.price_net + item.shipping_net
        items.append(
            {
                'id': item.pk,
                'price': item.price_net + item.shipping_net,
                'quantity': data_name['quantity'],
                'props': data_name
            }
        )

    context = {
        'total_price': total_price,
        'items': items,
        'delivery_address': order_group.delivery_address,
        'billing_address': order_group.billing_address,
    }

    return render(
        request,
        template_name='order/review.html',
        context=context
    )


@login_required(login_url='/login_signup/')
def checkout(request):
    context = {

    }

    return render(request, template_name='order/checkout.html', context=context)


@login_required(login_url='/login_signup/')
def complete(request):

    context = {

    }

    return render(request, template_name='order/complete.html', context=context)
