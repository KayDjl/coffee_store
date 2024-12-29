from django import template

from carts.models import Cart
from users.models import User
from django.db.models import F, Sum, ExpressionWrapper, DecimalField
from django.db.models.functions import Coalesce

register = template.Library()

@register.filter
def sum_all_total(carts):
    """
    Суммирует значения total_price для всех объектов в корзине.
    """
    # return sum(cart.total_price for cart in carts)

    total_price = carts.annotate(
        item_total_price = ExpressionWrapper(
            (F('product__price') + Coalesce(Sum(F('toppings__price')), 0)) * F('quantity'),
            output_field=DecimalField())).aggregate(
            total_price=Sum(F('item_total_price'))
        )['total_price']
    
    return total_price
    
    
         
         