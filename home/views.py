from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class HomeView(TemplateView):
    template_name = "home_page/index.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super(HomeView, self).get_context_data(*args, **kwargs)
        return context_data
