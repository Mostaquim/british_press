from django.shortcuts import render, HttpResponse, Http404
from clients.models import Orders
from django.middleware.csrf import get_token
from .helpers import place_order
# Create your views here.


def confirm_order(request, pk):
    order = Orders.objects.filter(pk=pk)
    if request.method == 'POST':
        if request.POST.get('uploaded_file'):
            uploaded_file = request.POST.get('uploaded_file')
            if place_order(pk,uploaded_file):
                return HttpResponse('Order Confirmed')


    if not order.exists():
        raise Http404

    order = order[0]

    context = {
        'order': order,
        'csrf': get_token(request)
    }

    return render(request, template_name='clients/confirm_order.html', context=context)
