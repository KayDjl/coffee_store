from django.db import models
from django.utils.timezone import now
from users.models import User

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название новости")
    slug = models.SlugField(max_length=200, blank=True, null=True, verbose_name="Slug")
    content = models.TextField(verbose_name="Текст новости")
    image = models.ImageField(upload_to='news_images/', verbose_name="Фото", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    views = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, verbose_name="Автор", default="Неизвестынй автор")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ("id", )
    
    def __str__(self):
        return self.title
    


class Comment(models.Model):
    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, verbose_name="Пользователь", default="Удаленный пользователь")
    text = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(default=now, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментарии"
        ordering = ("id", )

    def __str__(self):
        return f"Комментарий от {self.user.username} к {self.news.title}"