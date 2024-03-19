from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.MyLogin.as_view(), name='login'),
    path('logout/', views.logout, name='logout')
]