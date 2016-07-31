from django.contrib import admin

# Register your models here.

from forum.models import *
admin.site.register([Question,Answer,Comment,Profile])