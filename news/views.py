from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.views.generic.edit import FormMixin
from news.forms import CommentForm, CreateNewsForm
from .models import News
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from unidecode import unidecode
# from .forms import NewsForm, CommentForm


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    ordering = ['-created_at']  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список новостей'  
        return context


class NewsCreateView(UserPassesTestMixin, CreateView):
    model = News
    form_class = CreateNewsForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news:news_list')


    def form_valid(self, form):
        self.object = form.save(commit=False)
        if not self.object.slug:
            self.object.slug = slugify(unidecode(self.object.title))
            while News.objects.filter(slug=self.object.slug).exists():
                self.object.slug = f"{slugify(unidecode(self.object.title))}-{News.objects.filter(slug__startswith=self.object.slug).count() + 1}"
        self.object.author = self.request.user  
        self.object.save()  
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff
    
class NewsDeleteView(UserPassesTestMixin, DeleteView):
    model = News
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news:news_list') 
    def test_func(self):
        return self.request.user.is_staff
    

class NewsDetailView(FormMixin, DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    form_class = CommentForm 

    def get_success_url(self):
        # Перенаправление после успешного добавления комментария
        return reverse('news:news_detail', kwargs={'slug': self.object.slug})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        session_key = f'viewed_news_{self.object.pk}'

        # Если в сессии нет ключа для этой новости, засчитываем просмотр
        if not request.session.get(session_key, False):
            self.object.views += 1
            self.object.save(update_fields=['views'])
            request.session[session_key] = True  # Отмечаем просмотр в сессии

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Обрабатываем POST-запрос для добавления комментария
        self.object = self.get_object()
        if not request.user.is_authenticated:
            messages.warning(self.request, "Что бы оставить коментарий, войдите в сисему.")
            return redirect(reverse('users:login'))
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = self.object
            comment.user = request.user
            comment.save()
            messages.success(request, "Ваш комментарий был успешно добавлен.")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
        

