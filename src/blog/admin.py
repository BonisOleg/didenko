from django.contrib import admin
from unfold.admin import ModelAdmin

from src.blog.models import Category, Post
from src.core.admin_tinymce import TinyMCEAdminMixin


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('title', 'slug', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Post)
class PostAdmin(TinyMCEAdminMixin, ModelAdmin):
    list_display = (
        'title',
        'category',
        'is_featured',
        'is_published',
        'published_at',
    )
    list_filter = ('is_published', 'is_featured', 'category')
    list_editable = ('is_featured', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug', 'excerpt')
    date_hierarchy = 'published_at'
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'title',
                    'slug',
                    'category',
                    'excerpt',
                    'body',
                    'cover_image',
                    'cover_alt',
                ),
            },
        ),
        (
            'Публікація',
            {
                'fields': ('is_published', 'is_featured', 'published_at'),
            },
        ),
        (
            'SEO',
            {
                'fields': ('seo_title', 'seo_description', 'seo_h1'),
                'classes': ('collapse',),
            },
        ),
    )
