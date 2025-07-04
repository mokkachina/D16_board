from django import template
import post.views as views
from post.models import Category, TagPost
from post.utils import menu

register = template.Library()

@register.simple_tag
def get_menu():
    return menu

@register.inclusion_tag('board/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats':cats, 'cat_selected': cat_selected}

@register.inclusion_tag('board/list_tags.html')
def show_all_tags():
    return {'tags': TagPost.objects.all()}