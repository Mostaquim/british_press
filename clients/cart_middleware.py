from clients.models import CartItems


class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # oldTODO PROCESS THE CART INFO HERE
        # @ IF USER has CART ITEMS
        # @ IF SESSION HAS CART ITEMS
        # @ request.cart = items

        if request.user.is_authenticated:
            items = CartItems.objects.filter(user=request.user)
            request.CART = items
        else:
            if 'cart' in request.session:
                cart = request.session['cart']
                items = CartItems.objects.filter(pk__in=cart)
                request.CART = items
            else:
                request.CART = None

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
