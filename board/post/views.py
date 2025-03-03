from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse
from django.template.loader import render_to_string



menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'},
]
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
    return render(reqest, 'board/about.html', {"title":"О сайте", 'menu': menu})

def show_post(reqest, post_id):
    return HttpResponse(f'Отображение статьи с id ={post_id}')

def addpage(request):
    return HttpResponse('Добавление статьи')
def contact(request):
    return HttpResponse('Обратная связь')
def login(request):
    return HttpResponse('Авторизация')


def page_not_found(reqest, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
