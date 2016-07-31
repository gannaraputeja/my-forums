from django.core.urlresolvers import reverse
from django.forms.models import ModelForm
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django import template

from forum.forms import *
from forum.models import *

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password')

@csrf_exempt
def adduser(request):
    url = reverse('homepage')
    if request.method == "POST":
        form = UserForm(request.POST)
    else :
        form = UserForm(request.GET)
    if form.is_valid():
        User.objects.create_user(**form.cleaned_data)
        Profile.objects.create(user=User.objects.get(username=form.cleaned_data['username']),username=form.cleaned_data['username'],gender="")
        url = reverse('profile-update', kwargs={'pk':Profile.objects.get(username=form.cleaned_data['username']).id})
    return HttpResponseRedirect(url)

def profileupdate(request):
    form = ProfileForm(request.user)
    template = loader.get_template("forum/Profile_update_form.html")
    return HttpResponse(template.render(context={'form':form}))

def homepage(request):
    profile = None
    if request.user.is_authenticated() :
        authenticated = True
        profile = Profile.objects.get(user_id=User.objects.get(username = request.user).id)
    else :
        authenticated = False
    suggestionform = SuggestionForm()
    subscribeform = SubscribeForm()
    form1 = UserForm()
    template = loader.get_template("homepage.html")
    return HttpResponse(template.render(context={'form1':form1,'authenticated':authenticated,'profile':profile,'suggestionform':suggestionform,'subscribeform':subscribeform}))

def profile(request):
    if request.user.is_authenticated() :
        profile = Profile.objects.get(username__exact=request.user)
        user = User.objects.get(username__exact=request.user)
        profileform = ProfileForm(request.user)
        template = loader.get_template("forum/profile.html")
        return HttpResponse(template.render(context={"user":user,"profile":profile,'profileform':profileform}))
    else :
        return HttpResponseRedirect(r'/login')

def questions(request):
    if request.user.is_authenticated() :
        questions = Question.objects.all()
        template = loader.get_template(r"forum/forums.html")
        result = template.render(context={"questions":questions})
        return HttpResponse(result)
    else :
        return HttpResponseRedirect(r'/login')

def question_answer_comment(request,pk):
    if request.user.is_authenticated() :
        question = Question.objects.get(id=pk)
        answers = Answer.objects.order_by("question_id")
        comments = Comment.objects.order_by("answer__question_id","answer_id")

        template = loader.get_template(r"forum/forum.html")

        answerform = AnswerForm()
        commentform = CommentForm()

        result = template.render(context={"question": question,"answers":answers,"comments":comments,"answerform":answerform,"commentform":commentform})
        return HttpResponse(result)
    else :
        return HttpResponseRedirect(r'/login')

@csrf_exempt
def answer(request,pk):
    if request.method == "POST":
        form = AnswerForm(request.POST)
    else :
        form = AnswerForm(request.GET)
    ans="none"
    if form.is_valid() :
        ans =  form.cleaned_data['answer']
    answer = Answer.objects.create(answer=ans,question=Question.objects.get(id=pk),user=User.objects.get(username__exact=request.user))
    answer.save()
    url = reverse('question_answer_comment',args=[pk])
    return HttpResponseRedirect(url)

@csrf_exempt
def comment(request,qid,aid):
    if request.method == "POST":
        form = CommentForm(request.POST)
    else :
        form = CommentForm(request.GET)
    com = "none"
    if form.is_valid() :
        com =  form.cleaned_data['comment']
    comment = Comment.objects.create(comment=com,answer=Answer.objects.get(id=aid),user=User.objects.get(username__exact=request.user))
    comment.save()
    url = reverse('question_answer_comment',args=[qid])
    return HttpResponseRedirect(url)

@csrf_exempt
def subscribe(request):
    sub = None
    name = ""
    if request.method == "POST" :
        form = SubscribeForm(request.POST)
    else :
        form = SubscribeForm(request.GET)
    if form.is_valid() :
        sub = form.cleaned_data['email']
        name = form.cleaned_data['name']
    subs = Subscribe.objects.create(email=sub,name=name)
    subs.save()
    url = reverse('homepage')
    return HttpResponseRedirect(url)

@csrf_exempt
def suggestion(request):
    sug = None
    name = ""
    if request.method == "POST" :
        form = SuggestionForm(request.POST)
    else :
        form = SuggestionForm(request.GET)
    if form.is_valid() :
        sug = form.cleaned_data['suggestion']
        name = form.cleaned_data['name']
    sugs = Suggestion.objects.create(suggestion=sug,name=name)
    sugs.save()
    url = reverse('homepage')
    return HttpResponseRedirect(url)

def accept(request,qid,aid):
    if request.method == "POST":
        if request.user == User.objects.get(username=Answer.objects.get(id=aid).user).username :
            value = Profile.objects.get(user=User.objects.get(username=request.user)).credits
            Profile.objects.get(user=User.objects.get(username=request.user)).update(credits=value+5)
    url = reverse('question_answer_comment', args=[qid])
    return HttpResponseRedirect(url)

