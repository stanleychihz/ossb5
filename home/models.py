from django.db import models
from datetime import datetime
from nudenet import NudeDetector
from django.shortcuts import render, redirect

# Create your models here.

class Students(models.Model):

    reg = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)
    program = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.reg + " " + self.name + " " + self.program
    

class Option(models.Model):

    title = models.CharField(max_length=100, null=True)
    img = models.ImageField(blank=True, upload_to='option_images/')
    location = models.CharField(null=True, max_length=100)

    def __str__(self):

        return self.title
    
class Category(models.Model):

    title = models.CharField(max_length=100, null=True)
    img = models.ImageField(blank=True, upload_to='category_images/')

    def __str__(self):

        return self.title
    
class UserIcon(models.Model):

    img = models.ImageField(blank=True, upload_to='user_icon_images/')


class Icon2(models.Model):

    suggest = models.ImageField(null=True, upload_to=('home_icon/'))
    inbox = models.ImageField(null=True, upload_to=('home_icon/'))
    outbox = models.ImageField(null=True, upload_to=('home_icon/'))
    inprivate = models.ImageField(null=True, upload_to=('home_icon/'))

class Icon(models.Model):

    edit = models.ImageField(null=True, upload_to=('home_icon/'))
    comment = models.ImageField(null=True, upload_to=('home_icon/'))
    delete = models.ImageField(null=True, upload_to=('home_icon/'))
    like = models.ImageField(null=True, upload_to=('home_icon/'))
    back = models.ImageField(null=True, upload_to=('home_icon/'))
    image = models.ImageField(null=True, upload_to=('home_icon/'))
    audio = models.ImageField(null=True, upload_to=('home_icon/'))
    video = models.ImageField(null=True, upload_to=('home_icon/'))


    
class Messages(models.Model):
    pkv  = models.IntegerField(primary_key=True)
    cat = models.CharField(max_length=100, null=True)
    reg = models.CharField(max_length=100, null=True)
    identity = models.CharField(max_length=100, null=True)
    msg = models.CharField(max_length=10000, blank=True)
    reply = models.CharField(max_length=10000, blank=True)
    no_comments = models.CharField(max_length=100, null=True)
    no_likes  = models.CharField(max_length=100, null=True)
    nickname = models.CharField(max_length=100, blank=True)
    screenshot = models.ImageField(blank=True, upload_to='proof_screenshot/', null=True)
    image = models.ImageField(blank=True, upload_to='proof_images/', null=True)
    image2 = models.ImageField(blank=True, upload_to='proof_images2/', null=True)
    video = models.FileField(blank=True, upload_to='proof_video/', null=True)
    audio = models.FileField(blank=True, upload_to='proof_audio/', null=True)
    time = models.TimeField(auto_now=True, blank=False, null=True)
    timestamp = models.DateField(auto_now=True, blank=False, null=True)

    def __str__(self):

        return self.pkv and self.reg

    
class Likes(models.Model):
   
    pkv = models.CharField(max_length=100, null=True)
    reg = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, null=True)
    like = models.CharField(max_length=100, blank=True, null=True)
    replied = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):

        return self.pkv
    
    
class Comments(models.Model):
   
    pkv = models.CharField(max_length=100, null=True)
    reg = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, null=True)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    msg = models.CharField(max_length=10000, blank=True, null=True)
    replied = models.CharField(max_length=100, blank=True, null=True)
    msg_replied = models.CharField(max_length=10000, blank=True, null=True)
    timestamp = models.DateTimeField(default=datetime.now, blank=True, null=True)

    def __str__(self):

        return self.reg
    

class Replys(models.Model):
    pkv  = models.IntegerField(primary_key=True)
    reply = models.CharField(max_length=10000, blank=True)
    image = models.ImageField(blank=True, upload_to='admin_images/', null=True)
    video = models.FileField(blank=True, upload_to='admin_video/', null=True)
    audio = models.FileField(blank=True, upload_to='admin_audio/', null=True)
    time = models.TimeField(auto_now=True, blank=False, null=True)

    def __str__(self):

        return self.reply
    
class Chart_Type(models.Model):

    ids = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    name2 = models.CharField(max_length=50, null=True)

    def __str__(self):

        return self.name