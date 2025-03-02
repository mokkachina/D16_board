from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse
from django.template.loader import render_to_string


menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]

data_db = [
    {'id': 1, 'title': "Автомобили", 'content': "ВАЗ", 'is_published': True},
    {'id': 2, 'title': "Бытовые приборы", 'content': "Миксер", 'is_published': True},
    {'id': 3, 'title': "Дача", 'content': "Рассада", 'is_published': True}
]

def index(reqest):
    # t = render_to_string('board/index.html')
    # return HttpResponse(t)
    data = {
        "title": "Главная страница",
        'menu': menu,
        "posts": data_db,
    }
    return render(reqest, 'board/index.html', context=data)

def about(reqest):
    return render(reqest, 'board/about.html', {"title":"О сайте"})

def categories(reqest, cat_id):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}</p>")

def categories_by_slug(reqest, cat_slug):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>")

def archive(reqest, year):
    if year > 2025:
        uri = reverse('cats', args=('home_device',))
        return redirect(uri)
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")

def page_not_found(reqest, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
