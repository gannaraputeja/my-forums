from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView ,DeleteView
from django.contrib.auth.decorators import login_required
from models import *

@method_decorator(login_required,name='dispatch')
class QuestionCreateView(CreateView):
    model = Question

    fields = ['title','question','tags']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(QuestionCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('questions_list')

@method_decorator(login_required,name='dispatch')
class ProfileUpdateView(UpdateView):
    model = Profile

    fields = ['gender','dob']

    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('profile_view',kwargs={'pk':Profile.objects.get(username=self.request.user).id})

@method_decorator(login_required,name='dispatch')
class ProfileDetailView(DetailView):
    model = Profile

    def get_object(self, queryset=None):
        id = self.kwargs.get('pk')
        query = Profile.objects.all().get(id=id)
        return query

    def form_valid(self, form):
        print self.request.FIlES['avatar']
        return super(ProfileDetailView, self).form_valid(form)