from django import template

register = template.Library()

@register.filter
def sum_total(carts):
    """
    Суммирует значения total_price для всех объектов в корзине.
    """
    return sum(cart.total_price for cart in carts)