from decimal import Decimal

from django.contrib.auth.models import User, AnonymousUser
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.datastructures import SortedDict

from .cart_modifiers.loader import get_cart_item_modifiers


class CartManager(models.Manager):

    def get_for_request(self, request):
        if request.user.is_authenticated():
            return self.get_or_create(user=request.user)[0]
        if 'cart' in request.session:
            try:
                return self.get(pk=request.session['cart'])
            except self.model.DoesNotExist:
                pass
        cart = self.create(user=None)
        request.session['cart'] = cart.pk
        return cart


class Cart(models.Model):

    user = models.OneToOneField(User, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __init__(self, *args, **kwargs):
        super(Cart, self).__init__(*args, **kwargs)
        self.modifiers = SortedDict()
        self.reset_cached_items()

    def reset_cached_items(self):
        self.cached_items = self.items.all()

    def get_selected_items(self):
        return [item for item in self.cached_items if item.is_selected]

    def get_held_items(self):
        held_items = []
        for item in self.cached_items:
            if item.is_available and item.is_in_stock and item.is_held:
                held_items.append(item)
        return held_items

    def get_unavailable_items(self):
        unavailable_items = []
        for item in self.cached_items:
            if not item.is_available or not item.is_in_stock:
                unavailable_items.append(item)
        return unavailable_items

    @property
    def price(self):
        price = Decimal('0.00')
        for item in self.items.all():
            if item.is_selected:
                price += item.total_price
        return price

    @property
    def total_price(self):
        total_price = self.price
        for modifier in get_cart_modifiers():
            total_price = modifier(self, total_price)
        return total_price

    def add(self, product, quantity=1):
        item, created = self.items.get_or_create(
            product_type = ContentType.objects.get_for_model(product),
            product_id = product.pk,
            defaults = {'quantity': quantity},
        )
        if not created:
            item.quantity += quantity
            item.save()
        self.reset_cached_items()
        return item


class CartItem(models.Model):

    cart = models.ForeignKey(Cart, related_name='items')

    product_type = models.ForeignKey(ContentType)
    product_id = models.PositiveIntegerField()
    product = generic.GenericForeignKey('product_type', 'product_id')

    quantity = models.PositiveIntegerField(default=False)
    is_held = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        unique_together = ('cart', 'product_type', 'product_id')

    def __init__(self, *args, **kwargs):
        super(CartItem, self).__init__(*args, **kwargs)
        self.modifiers = SortedDict()

    @property
    def is_available(self):
        return getattr(self.product, 'is_available', True)

    @property
    def is_in_stock(self):
        return getattr(self.product, 'is_in_stock', True)

    @property
    def is_selected(self):
        return self.is_available and self.is_in_stock and not self.is_held

    @property
    def unit_price(self):
        return self.product.price

    @property
    def price(self):
        return self.unit_price * self.quantity

    @property
    def total_price(self):
        self.modifiers.clear()
        total_price = self.price
        for modifier in get_cart_item_modifiers():
            total_price = modifier(self, total_price)
        return total_price
