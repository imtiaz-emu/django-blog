from django import template
register = template.Library()

from django.utils import timezone
from ..models import Post


@register.simple_tag
def total_posts():
	return Post.objects.filter(status='published').count()

@register.inclusion_tag('blog/post/recent.html')
def recent_posts(count=5):
	latest_posts = Post.objects.filter(status='published', publish__lte=timezone.now()).order_by('-publish')[:count]
	return {'recent_posts': latest_posts}
