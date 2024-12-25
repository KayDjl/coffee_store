from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.generic import DetailView, ListView

from main.models import Products, Topping


class IndexView(ListView):
    model = Products
    template_name = 'main/index.html'
    context_object_name = "main"
    paginate_by = 8
    slug_url_kwarg = "category_slug"


    def get_queryset(self):
        category_slug = self.kwargs.get(self.slug_url_kwarg, 'all')
        order_by = self.request.GET.get("order_by")
        
        if category_slug == 'all':
            goods = super().get_queryset()
        else:
            goods = super().get_queryset().filter(category__slug=category_slug)
            if not goods.exists():
                return goods
        if order_by and order_by != 'default':
            goods = goods.order_by(order_by)

        return goods

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Coffe house"
        context["slug_url"] = self.kwargs.get(self.slug_url_kwarg, "all")
        return context


class productView(DetailView):
    template_name = 'main/product.html'
    slug_url_kwarg = "product_slug"
    context_object_name = 'product'

    def get_object(self, queryset=None):
        product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topping = Topping.objects.all()
        context["topping"] = topping
        context['title'] = "Coffee house"
        return context