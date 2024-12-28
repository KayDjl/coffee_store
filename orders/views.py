from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.db.models import F, Sum, ExpressionWrapper, DecimalField
from django.db.models.functions import Coalesce


from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = "orders/create_order.html"
    form_class = CreateOrderForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        print("form_valid вызван")
        try:
            with transaction.atomic():
                user = self.request.user
                cart_items = Cart.objects.filter(user=user)
                print(f"Cart items: {cart_items}")

                if cart_items.exists():
                     # Определяем значения для оплаты на основе выбора
                    payment_choice = form.cleaned_data["payment_on_get"]
                    is_paid = payment_choice == "0"
                    payment_on_get = payment_choice == "1"
                    # Создать заказ
                    order = Order.objects.create(
                        user=user,
                        phone_number=form.cleaned_data["phone_number"],
                        requires_delivery=form.cleaned_data["requires_delivery"],
                        delivery_address=form.cleaned_data["delivery_address"],
                        is_paid = is_paid,
                        payment_on_get = payment_on_get
                    )
                    # Создать заказанные товары
                    for cart_item in cart_items:
                        product = cart_item.product
                        name = cart_item.product.name
                        toppings = cart_item.toppings.all()
                        price = cart_item.total_price
                        quantity = cart_item.quantity

                        order_item = OrderItem.objects.create(
                            order=order,
                            product=product,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )
                        order_item.toppings.set(toppings)
                        product.save()

                    # Очистить корзину пользователя после создания заказа
                    cart_items.delete()

                    messages.success(self.request, "Заказ оформлен!")
                    print("Order created successfully")
                    return redirect("main:index")
        except ValidationError as e:
            print(f"Validation error: {e}")
            messages.success(self.request, str(e))
            return redirect("orders:create_order")
        
    def form_invalid(self, form):
        messages.error(self.request, "Форма содержит ошибки.")
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформление заказа'
        context['order'] = True

        user = self.request.user
        total_price = Cart.objects.filter(user=user).annotate(
            item_total_price = ExpressionWrapper(
                (F('product__price') + Coalesce(Sum(F('toppings__price')), 0)) * F('quantity'),
                output_field=DecimalField()
            )
        ).aggregate(
            total_price=Sum(F('item_total_price'))
        )['total_price']

        context['total_price'] = total_price

        return context