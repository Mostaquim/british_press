from django.shortcuts import render, HttpResponse, Http404
from clients.models import Orders
# Create your views here.


def confirm_order(request, pk):
    order = Orders.objects.filter(pk=pk)
    if not order.exists():
        raise Http404

    order = order[0]

    context = {
        'order': order
    }

    return render(request, template_name='clients/confirm_order.html', context=context)
