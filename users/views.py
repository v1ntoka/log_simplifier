from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from users.forms import MyAuthForm
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect, reverse


class MyLogin(LoginView):
    template_name = 'users/login_view.html'
    form_class = MyAuthForm
    success_url = reverse_lazy('upload:upload')


def my_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("users:login"))
