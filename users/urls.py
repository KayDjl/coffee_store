from django.urls import path

from users import views


app_name = "users"
urlpatterns = [
    path('login/', views.loginView.as_view(), name='login'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('logout/', views.logout, name='logout'),
]