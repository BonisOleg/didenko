from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def healthz(request):
    return HttpResponse('ok', content_type='text/plain')


def page_not_found(request, exception):
    return render(
        request,
        'pages/404.html',
        {'page_title': 'Сторінку не знайдено'},
        status=404,
    )


def server_error(request):
    return render(
        request,
        'pages/500.html',
        {'page_title': 'Помилка сервера'},
        status=500,
    )
