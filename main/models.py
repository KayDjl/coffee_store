from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")

    class Meta:
        db_table = "category"
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"
        ordering = ("id", )

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
    descriptions = models.TextField(blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(upload_to="product_images", blank=True, null=True, verbose_name="Изображение")
    structure = models.TextField(blank=True, null=True, verbose_name="Состав")
    weight = models.PositiveIntegerField(default=250, verbose_name="Вес")
    calories = models.PositiveIntegerField(default=0, verbose_name="Ккал")
    protein = models.DecimalField(default=0.0, max_digits=5, decimal_places=1, verbose_name="Белки")
    fats = models.DecimalField(default=0.0, max_digits=5, decimal_places=1, verbose_name="Жиры")
    carb = models.DecimalField(default=0.0, max_digits=5, decimal_places=1, verbose_name="Углеводы")
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(to=Categories, on_delete=models.SET_DEFAULT, verbose_name="Категория", default="Неизвестная категория")

    class Meta:
        db_table = "product"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("id", )

    def __str__(self):
        return self.name
    
class TypeTopping(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Тип добавки")
    class Meta:
        db_table = "typetop"
        verbose_name = "Тип добавки"
        verbose_name_plural = "Типы добавок"
        ordering = ("id", )

    def __str__(self):
        return self.name


class Topping(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    image = models.ImageField(upload_to="topping_images", blank=True, null=True, verbose_name="Изображение")
    calories = models.PositiveIntegerField(default=0, verbose_name="Ккал")
    protein = models.DecimalField(default=0.0, max_digits=5, decimal_places=1, verbose_name="Белки")
    fats = models.DecimalField(default=0.00, max_digits=5, decimal_places=1, verbose_name="Жиры")
    carb = models.DecimalField(default=0.00, max_digits=5, decimal_places=1, verbose_name="Углеводы")
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name="Цена")
    types = models.ForeignKey(to=TypeTopping, on_delete=models.SET_DEFAULT, verbose_name="Тип добавки", default="Неизвестный тип добавки")

    class Meta: 
        db_table = "topping"
        verbose_name = "Топинг"
        verbose_name_plural = "Топинги"

    def __str__(self):
        return self.name