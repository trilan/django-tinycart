from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, RequestFactory

from tinycart.models import Cart
from tinycart.views import CartItemListView

from .models import Book


class CartItemListViewTests(TestCase):

    def create_request(self, method, data=None):
        request = getattr(RequestFactory(), method)('/cart/', data=data or {})
        request.user = AnonymousUser()
        request.session = {}
        request.cart = Cart.objects.get_for_request(request)
        return request


class CartItemListViewGetTests(CartItemListViewTests):

    def setUp(self):
        self.view = CartItemListView.as_view()
        self.request = self.create_request()

        self.held_book = Book.objects.create()
        self.held_item = self.request.cart.add(self.held_book, is_held=True)

        self.available_book = Book.objects.create()
        self.available_item = self.request.cart.add(self.available_book)

        self.unavailable_book = Book.objects.create(is_available=False)
        self.unavailable_item = self.request.cart.add(self.unavailable_book)

    def create_request(self):
        return super(CartItemListViewGetTests, self).create_request('get')

    def test_context_data(self):
        c = self.view(self.request).context_data
        self.assertEqual(c['held_object_list'], [self.held_item])
        self.assertEqual(c['available_object_list'], [self.available_item])
        self.assertEqual(c['unavailable_object_list'], [self.unavailable_item])


class CartItemListViewPostTests(CartItemListViewTests):

    def setUp(self):
        self.view = CartItemListView.as_view()
        self.book = Book.objects.create()

    def create_request(self, data=None):
        return super(CartItemListViewPostTests, self).create_request('post', data)

    def test_add_to_cart(self):
        request = self.create_request({
            'product_id': self.book.pk,
            'product_type': ContentType.objects.get_for_model(Book).pk})
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(request.cart.items.count(), 1)

        item = request.cart.items.get()
        self.assertEqual(item.product, self.book)
        self.assertEqual(item.quantity, 1)
        self.assertFalse(item.is_held)

    def test_add_to_cart_with_quantity(self):
        request = self.create_request({
            'product_id': self.book.pk,
            'product_type': ContentType.objects.get_for_model(Book).pk,
            'quantity': 5})
        response = self.view(request)
        self.assertEqual(response.status_code, 302)

        item = request.cart.items.get()
        self.assertEqual(item.quantity, 5)
