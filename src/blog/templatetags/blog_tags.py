from django import template

from src.blog.selectors import post_badge_label, post_read_more_label

register = template.Library()


@register.filter
def blog_badge(post):
    return post_badge_label(post)


@register.filter
def blog_read_more(post):
    return post_read_more_label(post)
