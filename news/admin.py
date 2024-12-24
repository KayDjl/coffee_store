from django.contrib import admin
from .models import News, Comment

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'created_at', 'updated_at', 'views')
    prepopulated_fields = {"slug": ("title",)}  # Автозаполнение slug на основе title


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('news', 'user', 'created_at')
    search_fields = ('news__title', 'user__username', 'text')