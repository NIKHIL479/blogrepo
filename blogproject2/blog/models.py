from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()#.filter(status='published')

# Create your models here.
class Post(models.Model):

    STATUS_CHOICES=(('draft','Draft'),('published','Published'))
    title=models.CharField(max_length=256)
    slug=models.SlugField(max_length=234,unique=True)
    author=models.ForeignKey(User,related_name='blog_posts',on_delete=models.CASCADE)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)#system time
    created=models.DateTimeField(auto_now_add=True)#post object created time
    updated=models.DateTimeField(auto_now=True)#save method called time(we call save method to update an object)
    status=models.CharField(max_length=11,choices=STATUS_CHOICES,default='draft')
    objects=CustomManager()
    tags=TaggableManager()#Post.tags.all()

    class Meta:
        ordering=('-publish',)

    def __str__(self):
        return self.title

    #canonical or reverse url
    def get_absolute_url(self):
        return reverse('post_detail',args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])
#MODEL RELATED TO COMMENTS SECTION
class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    name=models.CharField(max_length=300)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)#post object created time
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    class Meta:
        ordering=('-created',)

    def __str__(self):
        return 'commented by {} on {}'.format(self.name,self.post)
