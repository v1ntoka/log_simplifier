from django.http import HttpResponse
from django.shortcuts import render
from core.uploader import Uploader, InvalidFileError


def upload(request):
    uploader = Uploader(request)
    if request.method == "POST":
        try:
            uploader.save()
        except InvalidFileError as e:
            return HttpResponse(e)
    return render(request, template_name='upload/upload_view.html', context={'form': uploader.form, "files": uploader.queryset.order_by('-date')})
