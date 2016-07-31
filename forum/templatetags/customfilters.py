from django import template
from forum.models import *

register = template.Library()

@register.filter()
def countanswers(questionid):
    return Answer.objects.all().filter(question_id=questionid).count()