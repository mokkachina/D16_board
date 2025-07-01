from xml.dom import ValidationErr

from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.template.defaultfilters import title
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError

from .models import  Category, Post, Response

@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЩЗИЙКЛМНОПРСТУФХЦЧШЩЬЪЭЮЯабвгдеёжзиклмнопрстуфхцчшщьъэюя0123456789-"
    code = 'russian'
    def __init__(self, message=None):
        self.message = message if message else "Долны присутствовать только русские символы, дефис и пробел."
    def __call__(self, value, *args, **kwargs):
        if not (set(value)) <= set(self.ALLOWED_CHARS):
            raise ValidationError(self.message, code=self.code)
class AddPostForm(forms.ModelForm):
    # title = forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-input'}),
    #                         validators=[
    #                             RussianValidator(),
    #                         ],)
    # slug = forms.SlugField(max_length=255, label='URL',
    #                        validators=[
    #                          MinLengthValidator(5, message='Минимум 5 символов'),
    #                          MaxLengthValidator(50, message='Максимум 50 символов'),
    #                        ])
    # content = forms.CharField(widget=forms.Textarea(), required=False, label='Контент')
    # is_published = forms.BooleanField(required=False, initial=True, label='Статус')
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана', label="Категории")

    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': "form-input"}),
            'content': forms.Textarea(attrs={'cols':50,  "rows":5}),
        }
        labels = {'slug':'URL'}
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длинна превышает 50 символов')
        return title
class UploadFileForm(forms.Form):
    file = forms.FileField(label='Фаил')

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Напишите ваш отклик здесь...'
            }),
        }