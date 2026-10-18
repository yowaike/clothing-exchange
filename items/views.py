from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>Сервис обмена одеждой</h1>")
