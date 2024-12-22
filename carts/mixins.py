from django.template.loader import render_to_string

from carts.models import Cart
from .utils import get_user_carts

class CartMixins:
    def get_cart(self, request, product=None, cart_id=None, toppings=None):
        """
        Возвращает один элемент корзины, если он существует.
        """
        if request.user.is_authenticated:
            query_kwargs = {"user": request.user}
        else:
            query_kwargs = {"session_key": request.session.session_key}

        if product:
            query_kwargs["product"] = product

        if cart_id:
            query_kwargs["id"] = cart_id

        cart_query = Cart.objects.filter(**query_kwargs)

        if toppings is not None:
            for cart_item in cart_query:
                existing_topping = set(cart_item.toppings.values_list("id", flat=True))
                new_toppings = set(toppings.values_list("id", flat=True))
                if existing_topping == new_toppings:
                    return cart_item
            return None
        else:
            return cart_query.first()
    


    def render_cart(self, request):
        """
        Рендерит HTML корзины с учетом текущего пользователя или сессии.
        """
        user_cart = get_user_carts(request)
        context = {"carts": user_cart}

        return render_to_string(
            "carts/includes/included_cart.html", context, request=request
        )