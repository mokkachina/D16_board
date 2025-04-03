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
    {'id': 1, 'title': "ВАЗ 2121", 'content': '''<h3>Нива 2121</h3> (код кузова ВАЗ-2121 для трёхдверной модели и ВАЗ-2131 для пятидверной, в разное время также выпускалась под названиями Lada Niva, LADA 4x4 и LADA Niva Legend) — советский и российский автомобиль повышенной проходимости — внедорожник малого класса с несущим кузовом и постоянным полным приводом. Серийно производится с 5 апреля 1977 года (до 2006 года продавался под именем ВАЗ-2121 «Ни́ва» на внутреннем рынке, и как Lada Niva на экспортных рынках[2][3], с 2006''', 'is_published': True},
    {'id': 2, 'title': "Бытовые приборы", 'content': "Миксер", 'is_published': True},
    {'id': 3, 'title': "Ищу работу", 'content': "Ищу работу программиста", 'is_published': True}
]
cats_db = [
    {'id': 1, 'name': "Гилдмастеры"},
    {'id': 2, 'name': "ДД"},
    {'id': 3, 'name': "Зельевары"},
    {'id': 4, 'name': "Квестгиверы"},
    {'id': 5, 'name': "Кожевники"},
    {'id': 6, 'name': "Кузнецы"},
    {'id': 7, 'name': "Танки"},
    {'id': 8, 'name': "Торговцы"},
    {'id': 9, 'name': "Мастера заклинаний"},
    {'id': 10, 'name': "Хилы"},

]



def index(reqest):
    # t = render_to_string('board/index.html')
    # return HttpResponse(t)
    data = {
        "title": "Главная страница",
        'menu': menu,
        "posts": data_db,
        "cat_selected": 0,
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
def show_category(request, cat_id):
    data = {
        "title": "Главная страница",
        'menu': menu,
        "posts": data_db,
        "cat_selected": cat_id,
    }
    return render(request, 'board/index.html', context=data)

def page_not_found(reqest, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
