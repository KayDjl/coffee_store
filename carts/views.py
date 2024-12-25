from django.http import JsonResponse
from django.views import View
from carts.models import Cart
from main.models import Products, Topping
from .mixins import CartMixins

class CartAddView(CartMixins, View):
    def post(self, request):
        print("POST данные:", request.POST)
        product_id = request.POST.get("product_id")
        topping_ids = request.POST.getlist('topping_ids[]')
        print("Topping IDs", topping_ids)

        product = Products.objects.get(id=product_id)
        toppings = Topping.objects.filter(id__in=topping_ids)

        cart = self.get_cart(request, product=product, toppings=toppings)
        if cart:
            cart.quantity += 1
            cart.save()
            if toppings.exists():
                cart.toppings.add(*toppings)
        else:
            cart = Cart.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key if not request.user.is_authenticated else None,
                product=product,
                quantity=1,
            )
            if toppings.exists():
                cart.toppings.set(toppings)

        response_data = {
            "message": "Товар добавлен в корзину",
            "cart_items_html": self.render_cart(request),
        }

        return JsonResponse(response_data)
    
    
class CartRemoveView(CartMixins, View):
    def post(self, request):
        cart_id = request.POST.get('cart_id')
        cart = self.get_cart(request, cart_id=cart_id)
        quantity = cart.quantity
        cart.delete()

        response_data = {
            "message": "Товар удален из корзины",
            "quantity_deleted": quantity,
            "cart_items_html": self.render_cart(request)
        }

        return JsonResponse(response_data)
