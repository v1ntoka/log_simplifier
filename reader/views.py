from django.shortcuts import render
from django.core.paginator import Paginator
# from core.handlers import actualize_filename
from core.reader import Reader
from reader.forms import Filters
from django.shortcuts import redirect


def reader(request, filename=None):
    if not filename:
        return redirect('upload:upload')
    log_reader = Reader(filename=filename, **request.POST)
    filters = Filters(request.POST)
    context = {'filters': filters}
    if filters.is_valid():
        paginator = Paginator(log_reader.read(), 1000)
        page_number = request.GET.get('page', default=1)
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
    return render(request, 'reader_view.html', context=context)
