from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from tinycart.models import Cart
from tinycart.cart_modifiers.loader import (
    get_cart_item_modifiers, clear_cart_item_modifiers_cache)

from .models import Book, Shirt


class CartModelTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.user = AnonymousUser()
        self.request.session = {}

    def test_cart_for_anonymous_user(self):
        cart = Cart.objects.get_for_request(self.request)
        self.assertIsNone(cart.user)
        self.assertIn('cart', self.request.session)
        self.assertEqual(self.request.session['cart'], cart.pk)
        self.assertEqual(Cart.objects.get_for_request(self.request), cart)

    def test_cart_for_authenticated_user(self):
        self.request.user = User.objects.create_user('john', 'john@example.com')
        cart = Cart.objects.get_for_request(self.request)
        self.assertEqual(cart.user, self.request.user)
        self.assertNotIn('cart', self.request.session)
        self.assertEqual(Cart.objects.get_for_request(self.request), cart)

    def test_cart_add(self):
        cart = Cart.objects.get_for_request(self.request)
        cart_item = cart.add(Shirt.objects.create())
        cart.add(cart_item.product, quantity=5)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.get().quantity, 6)

    def test_cart_price(self):
        cart = Cart.objects.get_for_request(self.request)
        self.assertEqual(cart.price, Decimal('0.00'))

        cart.add(Book.objects.create(storage_on_hand=10), quantity=10)
        self.assertEqual(cart.price, Decimal('35.00'))

        cart.add(Shirt.objects.create())
        self.assertEqual(cart.price, Decimal('45.00'))

        cart.add(Book.objects.create(storage_on_hand=10, is_available=False))
        self.assertEqual(cart.price, Decimal('45.00'))

        cart.add(Book.objects.create(storage_on_hand=0))
        self.assertEqual(cart.price, Decimal('45.00'))

        cart_item = cart.add(Book.objects.create(storage_on_hand=10))
        cart_item.is_held = True
        cart_item.save()
        self.assertEqual(cart.price, Decimal('45.00'))


class CartItemModelTests(TestCase):

    def setUp(self):
        if hasattr(settings, 'TINYCART_CART_ITEM_MODIFIERS'):
            self.old_TINYCART_CART_ITEM_MODIFIERS = settings.TINYCART_CART_ITEM_MODIFIERS
        settings.TINYCART_CART_ITEM_MODIFIERS = (
            'tinycart.tests.cart_modifiers.every_second_book_is_for_free',
        )
        clear_cart_item_modifiers_cache()

        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.user = AnonymousUser()
        self.request.session = {}
        self.cart = Cart.objects.get_for_request(self.request)

    def tearDown(self):
        delattr(settings, 'TINYCART_CART_ITEM_MODIFIERS')
        if hasattr(self, 'old_TINYCART_CART_ITEM_MODIFIERS'):
            settings.TINYCART_CART_ITEM_MODIFIERS = self.old_TINYCART_CART_ITEM_MODIFIERS
            delattr(self, 'old_TINYCART_CART_ITEM_MODIFIERS')
        clear_cart_item_modifiers_cache()

    def test_cart_item_price(self):
        cart_item = self.cart.add(Book.objects.create())
        self.assertEqual(cart_item.price, Decimal('3.50'))

        cart_item = self.cart.add(Book.objects.create(), quantity=3)
        self.assertEqual(cart_item.price, Decimal('10.50'))

    def test_cart_item_total_price(self):
        cart_item = self.cart.add(Book.objects.create())
        self.assertEqual(cart_item.total_price, Decimal('3.50'))

        cart_item.quantity += 1
        self.assertEqual(cart_item.total_price, Decimal('3.50'))

        cart_item.quantity += 1
        self.assertEqual(cart_item.total_price, Decimal('7.00'))

    def test_cart_item_is_available(self):
        cart_item = self.cart.add(Book.objects.create())
        self.assertTrue(cart_item.is_available)

        cart_item = self.cart.add(Book.objects.create(is_available=False))
        self.assertFalse(cart_item.is_available)

        cart_item = self.cart.add(Shirt.objects.create())
        self.assertTrue(cart_item.is_available)

    def test_cart_item_is_in_stock(self):
        cart_item = self.cart.add(Book.objects.create())
        self.assertFalse(cart_item.is_in_stock)

        cart_item = self.cart.add(Book.objects.create(storage_on_hand=10))
        self.assertTrue(cart_item.is_in_stock)

        cart_item = self.cart.add(Shirt.objects.create())
        self.assertTrue(cart_item.is_in_stock)
