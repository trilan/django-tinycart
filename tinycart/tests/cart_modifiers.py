from decimal import Decimal


def every_second_book_is_for_free(cart_item, total_price):
    amount = cart_item.unit_price * (cart_item.quantity // 2)
    cart_item.modifiers['Every second book is for free'] = -amount
    return total_price - amount


def ten_percent_discount(cart, total_price):
    amount = total_price * Decimal('0.10')
    cart.modifiers['10% discount'] = -amount
    return total_price - amount
