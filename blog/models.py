
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from taggit.managers import TaggableManager



class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="blog_posts")
    body = models.TextField()
    image = models.ImageField(upload_to="images/")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    uptade = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')

    tags = TaggableManager()


    class Meta:
        ordering = ('-publish',)
        verbose_name_plural = "postlar"

    def __str__(self):
        return self.title


    def get_absalute_url(self):
        return reverse('blog:post_detail',args=[self.publish.year,self.publish.month,self.publish.day, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    name = models.CharField(max_length=255)
    email  = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    activate = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
        verbose_name_plural = "Comentlar"

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
