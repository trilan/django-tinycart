from django.utils.functional import SimpleLazyObject
from tinycart.models import Cart


class CartMiddleware(object):

    def process_request(self, request):
        request.cart = SimpleLazyObject(
            lambda: Cart.objects.get_for_request(request)
        )


class HTTPMethodOverrideMiddleware(object):

    allowed_methods = ('PUT', 'DELETE')
    webform_content_types = ('application/x-www-form-urlencoded',
                              'multipart/form-data')

    def is_webform(self, request):
        content_type = request.META.get('CONTENT_TYPE')
        if not content_type:
            return False
        return content_type.split(';')[0] in self.webform_content_types

    def process_request(self, request):
        if request.method != 'POST':
            return
        method = request.META.get('HTTP_X_HTTP_METHOD_OVERRIDE')
        if method is None and self.is_webform(request):
            method = request.POST.get('_method')
        if method is None or method.upper() not in self.allowed_methods:
            return
        request.method = method.upper()
