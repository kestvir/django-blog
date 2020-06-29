from django import template
from ..models import Post

register = template.Library()


@register.simple_tag
def get_popular_posts():
    return Post.most_popular_five_posts()


@register.simple_tag
def get_post_categories():
    return Post.post_categories()


@register.simple_tag
def get_num_of_category_posts(category):
    return Post.post_categories_num(category)


@register.simple_tag
def get_post_archive():
    pass
    return Post.post_archive()
