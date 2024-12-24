from django.urls import path
from .views import NewsCreateView, NewsDeleteView, NewsDetailView, NewsListView


app_name = 'news'

urlpatterns = [
    path('news_list/', NewsListView.as_view(), name='news_list'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('delete/<slug:slug>/', NewsDeleteView.as_view(), name='news_delete'),
    path('<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
]
