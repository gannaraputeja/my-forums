from django import forms

class AnswerForm(forms.Form):
    answer = forms.CharField(max_length=200)

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=200)

class ProfileForm(forms.Form):
    username = forms.SlugField()
    gender = forms.CharField(max_length=10)
    avatar = forms.ImageField()
    dob = forms.DateField()

class SuggestionForm(forms.Form):
    name = forms.CharField(max_length=30)
    suggestion = forms.CharField(max_length=200)

class SubscribeForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=70,required=True)
