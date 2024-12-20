from django.urls import path

from main import views


app_name = "main"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<slug:category_slug>/', views.IndexView.as_view(), name='category'),
    path('product/<slug:product_slug>/', views.productView.as_view(), name='product'),
]
