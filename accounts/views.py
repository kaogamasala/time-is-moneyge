from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views import generic

from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignupForm
 
 
class SignUpView(CreateView):
    """form_class = SignupForm
    success_url = reverse_lazy('127.0.0.1:8000/')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        # self.objectにsave()されたユーザーオブジェクトが格納される
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid"""
        
    form_class = SignupForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

"""    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'"""


