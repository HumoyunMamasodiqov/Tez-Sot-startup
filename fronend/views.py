

from django.shortcuts import render
from django.http import HttpResponseNotFound

def test_404(request):
    return HttpResponseNotFound(render(request, '404.html'))


def home_view(request):
    return render(request, 'home.html')



def qosjso_view(request):
    return render(request, 'qosjso.html')
