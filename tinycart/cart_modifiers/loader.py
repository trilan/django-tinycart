from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from django.utils.functional import curry, memoize


_cart_modifiers_cache = {}
_cart_item_modifiers_cache = {}


def clear_cart_modifiers_cache():
    global _cart_modifiers_cache
    _cart_modifiers_cache.clear()


def clear_cart_item_modifiers_cache():
    global _cart_item_modifiers_cache
    _cart_item_modifiers_cache.clear()


def load_modifier(modifier_name):
    module_name, attr = modifier_name.rsplit('.', 1)
    try:
        module = import_module(module_name)
    except ImportError, e:
        raise ImproperlyConfigured(
            'Error importing modifier %s: "%s"' % (modifier_name, e))
    try:
        modifier = getattr(module, attr)
    except AttributeError, e:
        raise ImproperlyConfigured(
            'Error importing modifier %s: "%s"' % (modifier_name, e))
    return modifier


def get_modifiers(setting_name):
    modifiers = []
    for modifier_name in getattr(settings, setting_name, ()):
        modifiers.append(load_modifier(modifier_name))
    return modifiers


get_cart_modifiers = memoize(
    func = curry(get_modifiers, 'TINYCART_CART_MODIFIERS'),
    cache = _cart_modifiers_cache,
    num_args = 0,
)
get_cart_item_modifiers = memoize(
    func = curry(get_modifiers, 'TINYCART_CART_ITEM_MODIFIERS'),
    cache = _cart_item_modifiers_cache,
    num_args = 0,
)
