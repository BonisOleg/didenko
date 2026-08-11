from django.urls import path

from src.blog.views import (
    ApiBlogFeedView,
    ApiBlogMoreView,
    PostDetailView,
    PostListPartialView,
    PostListView,
)

app_name = 'blog'

urlpatterns = [
    path('blog/', PostListView.as_view(), name='list'),
    path('blog/partial/', PostListPartialView.as_view(), name='partial'),
    path('blog/<slug:slug>/', PostDetailView.as_view(), name='detail'),
    path('api/blog/', ApiBlogFeedView.as_view(), name='api_feed'),
    path(
        'api/blog/all/',
        ApiBlogFeedView.as_view(),
        {'api_category': 'all'},
        name='api_all',
    ),
    path(
        'api/blog/cases/',
        ApiBlogFeedView.as_view(),
        {'api_category': 'cases'},
        name='api_cases',
    ),
    path(
        'api/blog/news/',
        ApiBlogFeedView.as_view(),
        {'api_category': 'news'},
        name='api_news',
    ),
    path(
        'api/blog/tips/',
        ApiBlogFeedView.as_view(),
        {'api_category': 'tips'},
        name='api_tips',
    ),
    path('api/blog/more/', ApiBlogMoreView.as_view(), name='api_more'),
]
