from django.http import HttpResponse
from django.shortcuts import render, redirect
from upload import forms
from core.handlers import save_file_handler, get_files_list


def upload(request):
    form = forms.UploadForm()
    if request.method == "POST":
        form = forms.UploadForm(request.POST, request.FILES)
        if form.is_valid():
            filename = save_file_handler(request.FILES['file'])
            if filename:
                return redirect('reader:reader', filename=filename)
        else:
            return HttpResponse("<h1>Invalid file</h1>")
    return render(request, template_name='upload_view.html', context={'form': form, 'files': get_files_list()})
