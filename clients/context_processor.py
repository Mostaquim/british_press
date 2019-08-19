from clients.models import CartItems
from django.middleware.csrf import get_token


def cart_context(request):
    if request.session and 'cart' in request.session:
        s = request.session
        items = CartItems.objects.filter(pk__in=s['cart'])
        counts = items.count()
    else:
        counts = 0

    return {
        'cart_count' : counts,
        'csrf_token': get_token(request)
    }