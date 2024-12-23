from django import forms
from news.models import News

class CreateNewsForm(forms.Form):
    class Meta:
        model = News
        fields = ['title', 'content', 'image']

    title = forms.CharField()
    content = forms.CharField
    image = forms.ImageField(required=False)
   