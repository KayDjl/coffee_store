from django.db import models
from django.db.models import F, Sum, DecimalField, ExpressionWrapper
from django.db.models.functions import Coalesce
from main.models import Products, Topping
from users.models import User


class OrderitemQueryset(models.QuerySet):
    
    def total_price(self):
        total_price = self.annotate(
        item_total_price = ExpressionWrapper(
            (F('product__price') + Coalesce(Sum(F('toppings__price')), 0)) * F('quantity'),
            output_field=DecimalField())).aggregate(
            total_price=Sum(F('item_total_price'))
        )['total_price']
    
        return total_price
    


class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name="Пользователь", default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    requires_delivery = models.BooleanField(default=False, verbose_name="Требуется доставка")
    delivery_address = models.TextField( blank=True, null=True, verbose_name="Адрес доставки")
    payment_on_get = models.BooleanField(default=False, verbose_name="Оплата при получении")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    status = models.CharField(max_length=50, default="В обработке", verbose_name="Статус заказа")

    class Meta():
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("id", )

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(to=Products, on_delete=models.SET_DEFAULT, null=True, verbose_name="Продукт", default=None)
    name = models.CharField(max_length=150, verbose_name="Название")
    toppings = models.ManyToManyField(to=Topping, verbose_name="Топинг")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")

    objects = OrderitemQueryset.as_manager()

    class Meta():
        db_table = "order_item"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданныe товаы"
        ordering = ("id", )
            
    def products_price(self):
        toppings_price = sum(topping.price for topping in self.toppings.all())
        return round((self.price + toppings_price) * self.quantity, 2)

    
    def __str__(self):
        if self.name:
            return f"Товар {self.name} | Заказ № {self.order.pk}"
        return f"Товар без названия | Заказ № {self.order.pk}"