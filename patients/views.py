from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Patient, History, Diet
from django.shortcuts import get_object_or_404
import json
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.http import HttpResponseRedirect

# Create your views here.

class Home(TemplateView):
    template_name = 'patients/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Home, self).get_context_data(*args, **kwargs)
        patient = get_object_or_404(Patient, user=self.request.user)
        context["patient"] = patient
        chart_data = []
        for diet in patient.diets.all():
            temp = {}
            if diet.carbs:
                temp["Carbonhydrates"] = float(diet.carbs)
            if diet.fats:
                temp["Fats"] = float(diet.fats)
            if diet.dietary_fiber:
                temp["Dietary Fibres"] = float(diet.dietary_fiber)
            if diet.minerals:
                temp["Minerals"] = float(diet.minerals)
            if diet.proteins:
                temp["Proteins"] = float(diet.proteins)
            if diet.vitamins:
                temp["Vitmains"] = float(diet.vitamins)
            if diet.water:
                temp["Water"] = float(diet.water)
            chart_data.append(temp)
        context["diet_chart_data"] = json.dumps(chart_data)
        return context

    
class PatientEdit(UpdateView):
    model = Patient
    fields = ["dob", "blood_group", "genotype", "height", "weight", "gender"]
    template_name = "patients/patient_form.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PatientEdit, self).get_context_data(*args, *kwargs)
        context["patient"] = get_object_or_404(Patient, user=self.request.user)
        return context

    def get_object(self):
        return get_object_or_404(Patient, user=self.request.user)


class HistoryAdd(CreateView):
    model = History
    fields = ["diagnosis", "description", "correction", "date_occured"]
    template_name = "patients/history_form.html"
    success_url = reverse_lazy("patients:home")

    def get_context_data(self, *args, **kwargs):
        context = super(HistoryAdd, self).get_context_data(*args, *kwargs)
        context["patient"] = get_object_or_404(Patient, user=self.request.user)
        return context

    def form_valid(self, form):
        patient = get_object_or_404(Patient, user=self.request.user)
        form.instance.patient = patient
        return super(HistoryAdd, self).form_valid(form)


class HistoryEdit(UpdateView):
    model = History
    fields = ["diagnosis", "description", "correction", "date_occured"]
    template_name = "patients/history_form.html"
    success_url = reverse_lazy("patients:home")

    def get_context_data(self, *args, **kwargs):
        context = super(HistoryEdit, self).get_context_data(*args, *kwargs)
        context["patient"] = get_object_or_404(Patient, user=self.request.user)
        return context


class DietAdd(CreateView):
    model = Diet
    fields = ["carbs", "fats", "dietary_fiber", "minerals", "proteins", "vitamins", "water"]
    template_name = "patients/diet_form.html"
    success_url = reverse_lazy("patients:home")

    def get_context_data(self, *args, **kwargs):
        context = super(DietAdd, self).get_context_data(*args, *kwargs)
        context["patient"] = get_object_or_404(Patient, user=self.request.user)
        return context

    def form_valid(self, form):
        patient = get_object_or_404(Patient, user=self.request.user)
        form.instance.patient = patient
        return super(DietAdd, self).form_valid(form)

class DietEdit(UpdateView):
    model = Diet
    fields = ["carbs", "fats", "dietary_fiber", "minerals", "proteins", "vitamins", "water"]
    template_name = "patients/diet_form.html"
    success_url = reverse_lazy("patients:home")

    def get_context_data(self, *args, **kwargs):
        context = super(DietEdit, self).get_context_data(*args, *kwargs)
        context["patient"] = get_object_or_404(Patient, user=self.request.user)
        return context


class DietDelete(DeleteView):
    model = Diet
    success_url = reverse_lazy("patients:home")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
