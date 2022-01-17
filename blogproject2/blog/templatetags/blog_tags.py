from blog.models import Post
from django import template
register=template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.count()
@register.inclusion_tag('blog/latestposts123.html')
def show_latest_posts():
    latest_posts=Post.objects.order_by('-publish')[:8]
    return {'latest_posts':latest_posts}
