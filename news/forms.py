from django import forms
from news.models import Comment, News

class CreateNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

   