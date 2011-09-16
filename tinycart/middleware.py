from django.utils.functional import SimpleLazyObject
from tinycart.models import Cart


class CartMiddleware(object):

    def process_request(self, request):
        request.cart = SimpleLazyObject(
            lambda: Cart.objects.get_for_request(request)
        )
