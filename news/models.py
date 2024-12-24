from django.db import models
from django.utils.timezone import now
from unidecode import unidecode
from users.models import User
from django.utils.text import slugify

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название новости")
    slug = models.SlugField(max_length=200, blank=True, null=True, verbose_name="Slug")
    content = models.TextField(verbose_name="Текст новости")
    image = models.ImageField(upload_to='news_images/', verbose_name="Фото", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    views = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
            while News.objects.filter(slug=self.slug).exists():
                self.slug = f'{slugify(unidecode(self.title))}-{News.objects.filter(slug__startswith=self.slug).count() + 1}'
        super().save(*args, **kwargs)


class Comment(models.Model):
    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    text = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(default=now, verbose_name="Дата создания")

    def __str__(self):
        return f"Комментарий от {self.user.username} к {self.news.title}"