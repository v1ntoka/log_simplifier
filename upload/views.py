from django.http import HttpResponse
from django.shortcuts import render, reverse, redirect
from upload import forms
from core.handlers import create_temp_file
from django.urls import reverse_lazy


def upload(request):
    form = forms.UploadForm()
    if request.method == "POST":
        form = forms.UploadForm(request.POST, request.FILES)
        if form.is_valid():
            create_temp_file(request.FILES['file'])
            return redirect('reader:reader')
            # return HttpResponse(request.FILES)
        else:
            return HttpResponse("<h1>Invalid file</h1>")
    return render(request, template_name='upload_view.html', context={'form': form})
