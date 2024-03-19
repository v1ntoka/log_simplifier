from django.shortcuts import render
from django.core.paginator import Paginator
from core.reader import Reader
from reader.forms import Filters
from django.shortcuts import redirect


def reader(request, filename=None):
    if not filename:
        return redirect('upload:upload')
    log_reader = Reader(filename=filename, **request.POST)
    filters = Filters(log_reader.filters)
    context = {'filters': filters, 'filename': filename}
    if filters.is_valid():
        paginator = Paginator(log_reader.read(), 1000)
        page_number = request.GET.get('page', default=1)
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
    return render(request, 'reader/reader_view.html', context=context)
