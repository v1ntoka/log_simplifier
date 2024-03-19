from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import render
from users.forms import MyAuthForm


class MyLogin(LoginView):
    template_name = 'users/login_view.html'
    form_class = MyAuthForm


def my_logout(request):
    logout(request)
    return render(request, 'users/logout_done_view.html')
