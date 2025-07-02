from gc import get_objects

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template.defaultfilters import title
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from post.models import Post, Category, TagPost, UploadFiles
from post.forms import AddPostForm, UploadFileForm
from post.utils import DataMixin
from .models import Response
from .forms import ResponseForm



class PostHome(DataMixin, ListView):
    # model = Post
    template_name = 'board/index.html'
    context_object_name = 'posts'
    title_page = "Главная страница"
    cat_selected = 0


    def get_queryset(self):
        return Post.published.all().select_related('cat')

@login_required
def about(request):
    contact_list = Post.published.all()
    paginator = Paginator(contact_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'board/about.html',
                  {"title":"О сайте",  'page_obj': page_obj})


class ShowPost(DataMixin, DetailView):
    template_name = 'board/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context, title=context['post'].title)

        # Добавляем отклики к контексту
        if self.request.user.is_authenticated:
            context['responses'] = Response.objects.filter(
                post=self.object
            ).select_related('author').order_by('-created_at')

        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Post.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'board/addpost.html'
    success_url = reverse_lazy("home")
    title_page = 'Добавление статьи'
    permission_required = 'board.add_post'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

class UpdatePage(DataMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'board/addpost.html'
    success_url = reverse_lazy("home")
    title_page = "Редактирование статьи"
# class DeletePage(DeleteView):
#     model = Post
#     fields = ['title', 'content', 'photo', 'is_published', 'cat']
#     template_name = 'board/addpost.html'
#     success_url = reverse_lazy("home")
#     extra_context = {
#         'menu': menu,
#         "title": "Удаление статьи",
#     }

def contact(request):
    return HttpResponse('Обратная связь')
def login(request):
    return HttpResponse('Авторизация')


class PostCategory(DataMixin, ListView):
    template_name = 'board/index.html'
    context_object_name = 'posts'
    allow_empty = False


    def get_queryset(self):
        return Post.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория' + cat.name,
                                      cat_selected=cat.pk,
                                      )


def page_not_found(reqest, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class TagPostList(DataMixin, ListView):
    template_name = 'board/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None,**kwargs):
        context = super().get_context_data( **kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег:' + tag.tag)


    def get_queryset(self):
        return Post.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


class CreateResponseView(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm
    template_name = 'board/create_response.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, slug=self.kwargs['post_slug'])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        # Используем существующее имя URL 'post' вместо 'post_detail'
        return reverse('post', kwargs={'post_slug': self.object.post.slug})


class UserResponsesView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'board/user_responses.html'
    context_object_name = 'responses'
    paginate_by = 10

    def get_queryset(self):
        # Получаем только отклики на объявления текущего пользователя
        queryset = Response.objects.filter(post__author=self.request.user)

        # Фильтрация по статусу
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Фильтрация по объявлению
        post_id = self.request.GET.get('post')
        if post_id:
            queryset = queryset.filter(post_id=post_id)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст все объявления пользователя для фильтра
        context['user_posts'] = Post.objects.filter(author=self.request.user)
        return context


class UpdateResponseStatusView(LoginRequiredMixin, UpdateView):
    model = Response
    fields = ['status']
    template_name = 'board/update_response_status.html'

    def get_queryset(self):
        # Разрешаем изменять только отклики на свои объявления
        return super().get_queryset().filter(post__author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('user_responses')


class DeleteResponseView(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'board/delete_response.html'

    def get_queryset(self):
        # Разрешаем удалять только отклики на свои объявления
        return super().get_queryset().filter(post__author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('user_responses')