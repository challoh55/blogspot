from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    USERNAME_FIELD = 'username'
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=159)
    last_name = models.CharField(max_length=159)
    phonenumber = models.CharField(max_length=20)
    dob = models.DateField(null=True)
    image = models.ImageField(upload_to='profile_pics')


class NewPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='profile_pics')
    likes = models.ManyToManyField(User, related_name='blog_posts')

    #counting all comments related to a particulars post
    def comment_count(self):
        return self.comment_set.all().count()
    
    def total_likes(self):
        return self.likes.count()
    
    
    
    @classmethod
    def newpost_count(cls):
        return cls.objects.values('title').annotate(post_count=models.Count('title')).order_by('-post_count')
    
    @classmethod
    def most_comments_count(cls):
        return cls.objects.values('id','title', 'content', 'created_at', 'image',).annotate(post_count=models.Count('comment')).order_by('-post_count')


    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(NewPost, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


