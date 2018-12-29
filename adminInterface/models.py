from django.db import models
from django.contrib.auth.models import User
from markdown import markdown
from django.utils.html import mark_safe
from django.utils.text import Truncator
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Articles(models.Model):
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    title = models.CharField(max_length=100,unique=True)
    content = models.TextField(max_length=40000)
    date_added = models.DateTimeField(auto_now_add=True)
    pics = models.FileField(upload_to='topic_image/')

    def __str__(self):
        turncated_message = Truncator(self.content)
        return turncated_message.chars(100)

    def get_last_ten_posts(self):
        return self.order_by('-date_added')[:10]

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.content, safe_mode='escape'))
    
class Questions(models.Model):
    email = models.CharField(max_length=55)
    question = models.CharField(max_length=400)
    answer = models.TextField(max_length=4000,default='not answered')
    answered = models.BooleanField(default=False)
    answered_by = models.ForeignKey(User,related_name='ques',on_delete=models.CASCADE,blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class Report(models.Model):
    topic = models.CharField(max_length=80)
    description = models.TextField(max_length=4000)
    email = models.CharField(max_length=55)
    resolved = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic
    
    