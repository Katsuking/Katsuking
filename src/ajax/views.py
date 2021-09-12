from django.shortcuts import render
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
# Create your views here.


def index(request):
    return render(request, 'ajax/index.html', {})

def ajax_number(request):
    number1 = int(request.POST.get('number1'))
    number2 = int(request.POST.get('number2'))
    plus = number1 + number2
    minus = number1 - number2
    d = {
        'plus': plus,
        'minus': minus,
    }
    return JsonResponse(d)