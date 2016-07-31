from django.conf.urls import url

from forum import views
from forum.classviews import *

urlpatterns = [
    url(r'^profile/(?P<pk>[0-9]+)/update$',ProfileUpdateView.as_view(),name='profile-update'),

    url(r'^homepage$',views.homepage,name='homepage'),
    url(r'^register/$', views.adduser,name='register'),
    url(r'^profile/(?P<pk>[0-9]+)/view',ProfileDetailView.as_view(),name='profile_view'),
    url(r'^question/create$',QuestionCreateView.as_view(),name='questions-create'),
    url(r'^questions/$', views.questions, name='questions_list'),
    url(r'^questions/(?P<pk>[0-9]+)$', views.question_answer_comment, name='question_answer_comment'),
    url(r'^answer/create/(?P<pk>[0-9]+)$',views.answer,name="answer"),
    url(r'^comment/create/(?P<qid>[0-9]+)/(?P<aid>[0-9]+)$',views.comment,name="comment"),
    url(r'^subscribe$',views.subscribe,name='subscribe'),
    url(r'^suggestions',views.suggestion,name='suggestions'),
]