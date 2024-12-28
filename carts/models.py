from django.db import models
from main.models import Products, Topping
from users.models import User


class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    product = models.ForeignKey(to=Products, on_delete=models.SET_DEFAULT, verbose_name='Товар', default="Неизвестный товар")
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    session_key = models.CharField(max_length=32, null=True, blank=True, verbose_name='Ключ сессии')
    toppings = models.ManyToManyField(to=Topping, blank=True, verbose_name="Топпинги")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'Cart'
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
        ordering = ("id", )

    def __str__(self):
        if self.user:
            return f"Корзина {self.user.username} | Товар {self.product.name} | {self.quantity}"
        else:
            return f"Анонимная корзина | Товар {self.product.name} | {self.quantity}"

    @property
    def total_price(self):
        toppings_price = sum(topping.price for topping in self.toppings.all())
        return (self.product.price + toppings_price) * self.quantity
        

