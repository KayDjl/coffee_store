from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import News, Comment
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
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
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news:news_list') 

    def form_valid(self, form):
        news = News.objects.create(
            title=form.cleaned_data['title'],
            content=form.cleaned_data['content'],
            image=form.cleaned_data.get('image', None),
            author=self.request.user
        )
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff