from django.shortcuts import render
from django.views.generic import TemplateView
from patients.models import Patient, History, Diet
from django.db.models import F
# Create your views here.


class Home(TemplateView):
    template_name = "stats/home.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super(Home, self).get_context_data(*args, **kwargs)
        
        return context_data
