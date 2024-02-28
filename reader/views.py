from django.shortcuts import render
from django.core.paginator import Paginator
from core.handlers import file_reader
from reader.forms import Filters


def reader(request, filename=None):
    filters = Filters(request.POST)
    context = {'filters': filters}
    if filters.is_valid():
        paginator = Paginator(file_reader(**request.POST), 100)
        page_number = request.GET.get('page', default=1)
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
    return render(request, 'reader_view.html', context=context)
