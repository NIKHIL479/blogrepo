from django.shortcuts import render,get_object_or_404
from blog.models import Post
from django.core.paginator import *
from django.core.mail import send_mail
from blog.forms import EmailSendForm,CommentForm
from taggit.models import Tag#taggit is 3rd party application

# Create your views here.
#def post_list_view(request):
    #post_list=Post.objects.all()
    #return render(request,'blog/post_list.html',{'post_list':post_list})

def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()#QuerySet
    tag=None
    if tag_slug:#if tag_slug is not None
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])

    paginator=Paginator(post_list,3)
    page_number=request.GET.get('page')
    try:
        pageobj=paginator.page(page_number)#all records in this page_number will come
        print(type(pageobj))#<class 'django.core.paginator.Page'>
    except PageNotAnInteger:

        pageobj=paginator.page(1)#get records of page 1
    except EmptyPage:#if next page is empty
        pageobj=paginator.page(paginator.num_pages)#display last page

    return render(request,'blog/post_list.html',{'pageobj':pageobj,'tag':tag})

def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    comments=post.comments.filter(active=True)
    print('type of comments is')
    print(type(comments))
    csubmit=False
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
    else:
        form=CommentForm()
    return render(request,'blog/post_detail.html',{'post':post,'form':form,'csubmit':csubmit,'comments':comments})

def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    form=EmailSendForm()
    sent=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            subject='{}({}) recommends you to read {}'.format(cd['name'],cd['email'],post.title)
            post_url=request.build_absolute_uri(post.get_absolute_url())#/tt/<int:year>/<int:month>/<int:day>/<str:post> for post.get_absolute_url
            print(post_url)
            print(post.get_absolute_url)
            message='read post at:\n{}\n\n{}\'s comments:\n{}'.format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,cd['name'],[cd['to']],fail_silently=False)
            sent=True
    else:
        form=EmailSendForm()
    return render(request,'blog/sharebymail.html',{'form':form,'post':post,'sent':sent})
