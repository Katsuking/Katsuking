from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Club
from django.http import JsonResponse
from .forms import ClubsDataForm

# Create your views here.

"""class ClubChartView(TemplateView):
    template_name = 'clubs/chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"]= Club.objects.all() #"qs"は.chart.htmlの中で使えるわけ
        return context
        なんかpyplaneさん難しく書くよね。。。"""

    
def index(request):
    data= Club.objects.all()
    if request.method == 'POST':
        form = ClubsDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/clubs')
    else:
        form = ClubsDataForm()
    context = {
        'data':data,
        'form':form,
    }
    return render(request, 'clubs/chart.html', context)

