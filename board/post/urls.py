from django.urls import path, re_path, register_converter
from . import views
from. import converters
from .views import CreateResponseView, UserResponsesView, UpdateResponseStatusView, DeleteResponseView

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.PostHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.PostCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('edit/<int:pk>/', views.UpdatePage.as_view(), name='edit_page'),
    # path('del/<int:pk>/', views.DeletePage.as_view(), name='del_page'),
    path('response/<slug:post_slug>/', CreateResponseView.as_view(), name='create_response'),
    path('my-responses/', UserResponsesView.as_view(), name='user_responses'),
    path('response/<int:pk>/update/', UpdateResponseStatusView.as_view(), name='update_response'),
    path('response/<int:pk>/delete/', DeleteResponseView.as_view(), name='delete_response'),
]
