from django.urls import path
from django.contrib.auth.views import LoginView
from users import views, forms
from django.contrib.auth import logout

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name="users/login_view.html", form_class=forms.MyAuthForm), name='login'),
    path('logout/', views.my_logout, name='logout'),
]