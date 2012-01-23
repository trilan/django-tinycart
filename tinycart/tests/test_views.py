from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory

from tinycart.models import Cart
from tinycart.views import CartItemList

from .models import Book


class CartItemListTests(TestCase):

    def setUp(self):
        self.view = CartItemList.as_view()
        self.request = self.create_request()

        self.held_book = Book.objects.create()
        self.held_item = self.request.cart.add(self.held_book)
        self.held_item.is_held = True
        self.held_item.save()

        self.available_book = Book.objects.create()
        self.available_item = self.request.cart.add(self.available_book)

        self.unavailable_book = Book.objects.create(is_available=False)
        self.unavailable_item = self.request.cart.add(self.unavailable_book)

    def create_request(self):
        request = RequestFactory().get('/cart/')
        request.user = AnonymousUser()
        request.session = {}
        request.cart = Cart.objects.get_for_request(request)
        return request

    def test_context_data(self):
        c = self.view(self.request).context_data
        self.assertEqual(c['held_object_list'], [self.held_item])
        self.assertEqual(c['available_object_list'], [self.available_item])
        self.assertEqual(c['unavailable_object_list'], [self.unavailable_item])
