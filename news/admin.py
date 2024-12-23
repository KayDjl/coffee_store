from django.contrib import admin
from .models import News, Comment

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'views')
    search_fields = ('title', 'content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('news', 'user', 'created_at')
    search_fields = ('news__title', 'user__username', 'text')
