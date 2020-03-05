from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404
from .models import Expert, Qualification
from patients.models import Patient
# Create your views here.

class Home(TemplateView):
    template_name = "experts/home.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super(Home, self).get_context_data(*args, **kwargs)
        context_data["expert"] = get_object_or_404(Expert, user=self.request.user)
        return context_data


class QualificationView(TemplateView):
    template_name = "experts/qualification_view.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super(QualificationView, self).get_context_data(*args, **kwargs)
        pk = kwargs.get("pk")
        context_data["qualification"] = get_object_or_404(Qualification, pk=pk)
        return context_data


class QualificationEdit(View):
    def get(self, request, pk):
        if pk:
            qualification = get_object_or_404(Qualification, pk=pk)
        return render(self.request, 'experts/qualification_form.html', context={
            "qualification": qualification
        })


class Patients(TemplateView):
    template_name = "experts/patients.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super(Patients, self).get_context_data(*args, **kwargs)
        context_data["patients"] = Patient.objects.all()
        return context_data