from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import EmailSendForm, CommentForm
from django.core.mail import send_mail

# Create your views here.
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug = post,
                             publish__day = day,
                             publish__month = month,
                             publish__year = year)

    comments = post.comments.filter(status=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'form': comment_form})

def post_list(request):
    posts = Post.objects.filter(status = 'published')
    return render(request, 'blog/post/list.html', {'posts': posts})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailSendForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailSendForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})