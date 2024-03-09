from django.http import HttpResponse
from django.shortcuts import render, redirect
from upload import forms
from core.uploader import Uploader


def upload(request):
    uploader = Uploader(request)
    if request.method == "POST":
        uploader.save()
    #     form = forms.UploadForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         # filename = save_file_handler(request.FILES['file'])
    #         # if filename:
    #         #     return redirect('reader:reader', filename=filename)
    #     else:
    #         return HttpResponse(form.errors, status=400)

    return render(request, template_name='upload_view.html', context={'form': uploader.form})
