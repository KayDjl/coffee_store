from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.contrib import auth, messages
from carts.models import Cart
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm


class loginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse_lazy('users:logout'):
            return redirect_page
        return reverse_lazy('main:index')
    
    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                forgot_carts = Cart.objects.filter(user=user)
                session_carts = Cart.objects.filter(session_key=session_key)
                for session_cart in session_carts:
                    session_cart_toppings = set(session_cart.toppings.values_list("id", flat=True))
                    existing_cart = None
                    for forgot_cart in forgot_carts:
                        forgot_cart_toppings = set(forgot_cart.toppings.values_list("id", flat=True))
                        if (
                            forgot_cart.product == session_cart.product
                            and forgot_cart_toppings == session_cart_toppings
                        ):
                            existing_cart = forgot_cart
                            break
                    if existing_cart:
                        existing_cart.quantity += session_cart.quantity
                        existing_cart.save()
                    else:
                        session_cart.user = user
                        session_cart.session_key = None
                        session_cart.save()
                session_carts.delete()
            messages.success(self.request, f"{user.username}, Вы вошли в аккаунт")
                
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Coffe house - Авторизация"
        return context




class UserRegistrationView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance
        if user:
            form.save()
            auth.login(self.request, user)

        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(self.request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Coffee house - Регистрация'
        return context
    

class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлен")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Произошла ошибка')
        return super().form_invalid(form)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Личный кабинет'
        return context
    

    
@login_required
def logout(request):
    messages.success(request, f'{request.user.username}, Вы вышли из аккаунта')
    auth.logout(request)
    return redirect(reverse('main:index'))
    
