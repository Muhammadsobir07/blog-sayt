
from django.shortcuts import render,get_object_or_404
from .models import Post
from django.core.paginator import  Paginator,PageNotAnInteger, EmptyPage

from .forms import EmailPostForm,CommentForm
from django.core.mail import send_mail
from django.conf import settings

from taggit.models import Tag




def post_List(request,tag_slug=None):
    object_list = Post.objects.filter(status="published")

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 1)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(Paginator.num_pages)
    context = {
        "posts":posts,
        "page":page,
        "tag":tag,
    }
    return render(request, 'blog/post/list.html',context)





def post_detail(request,year,month,day,post):
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year = year,
        publish__month = month,
        publish__day = day 
    )
    
    comments = post.comments.filter(activate=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post 
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        "post":post,
        "comments":comments,
        "new_comment": new_comment,
        "comment_form":comment_form,
        
    }
    return render(request, 'blog/post/detail.html',context)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False 
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleand_date
            post_url = request.bulid_absalute_uri(post.get_absalute_url())
            subject = f"{cd['name']} sizga {post.title} ni oqishni tavsiya qiladi. "
            message = f"Salom yaxshimisiz . Quyidagi linkdagi postni oqib koring. {post_url}\n\nComents:{cd['comments']}"
            send_mail(subject,message,settings.EMAIL_HOST_USER, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

















