from django.contrib import admin
from main.models import Categories, Products, Topping, TypeTopping

admin.site.register(Topping)
admin.site.register(TypeTopping)

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}