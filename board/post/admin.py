from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, Category
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'tags']
    readonly_fields = ['post_photo']
    prepopulated_fields = {'slug': ("title",)}
    filter_horizontal = ['tags']
    list_display = ( 'title', 'post_photo', 'time_create', 'is_published')
    list_display_links =('title',)
    ordering = ('time_create', 'title')
    list_editable = ('is_published',)
    list_per_page = 3
    actions = ['set_published', 'set_draft']
    search_fields = ['title']
    save_on_top = True
    @admin.display(description="Изображение")
    def post_photo(self,  post: Post):
        if post.photo:
            return mark_safe(f"<img src='{post.photo.url}' width=50>")
        return "Без фото"
    @admin.action(description='Опубликовать')
    def set_published(self, request, queryset):
        queryset.update(is_published=Post.Status.PUBLISHED)

    @admin.action(description='Черновик')
    def set_draft(self, request, queryset):
        queryset.update(is_published=Post.Status.DRAFT)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
# admin.site.register(Post, CategoryAdmin, PostAdmin )