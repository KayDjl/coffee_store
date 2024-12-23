from django.urls import path
from .views import NewsCreateView, NewsListView


app_name = 'news'

urlpatterns = [
    path('news_list/', NewsListView.as_view(), name='news_list'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
]

 # path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    # path('<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
    # path('create/', CreateNewsView.as_view(), name='create_news'),