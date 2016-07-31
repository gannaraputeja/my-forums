from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.db import models


# Create your models here.
from django.template.defaultfilters import filesizeformat

from forums import settings


class Question(models.Model):
    title = models.CharField(max_length=30)
    question = models.CharField(max_length=200)
    tags = models.CharField(max_length=50)
    user = models.ForeignKey(User)

class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=200,null=True)
    user = models.ForeignKey(User)

class Comment(models.Model):
    answer = models.ForeignKey(Answer)
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(User)

class Profile(models.Model):
    user = models.ForeignKey(User)
    username = models.SlugField(max_length=50, unique=True, null=False)
    gender = models.CharField(max_length=10,null=True,blank=True)
    avatar = models.ImageField(upload_to='static/images/avatars/',null=True)
    hasavatar = models.BooleanField(default=False)
    dob = models.DateField(null=True,blank=True)
    acceptrate = models.IntegerField(default=0)
    credits = models.IntegerField(default=0)

class Suggestion(models.Model):
    name = models.CharField(max_length=30)
    suggestion = models.CharField(max_length=200,blank=True)

class Subscribe(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=70,null= True,unique= True,validators=[validate_email,])