from django.urls import path

from reader import views

app_name = 'reader'

urlpatterns = [
    path('', views.reader, name='reader'),
    path("<slug:filename>", views.reader, name='reader')

]
