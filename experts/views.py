from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404
from .models import Expert, Qualification
from patients.models import Patient
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PatientSerializer
# Create your views here.


class Home(LoginRequiredMixin, TemplateView):
    template_name = "experts/home.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super(Home, self).get_context_data(*args, **kwargs)
        context_data["expert"] = get_object_or_404(Expert, user=self.request.user)
        return context_data


class QualificationView(LoginRequiredMixin, TemplateView):
    template_name = "experts/qualification_view.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super(QualificationView, self).get_context_data(*args, **kwargs)
        pk = kwargs.get("pk")
        context_data["qualification"] = get_object_or_404(Qualification, pk=pk, expert__user=self.request.user)
        return context_data


class QualificationEdit(LoginRequiredMixin, View):
    def get(self, request, pk):
        if pk:
            qualification = get_object_or_404(Qualification, pk=pk, expert__user=self.request.user)
        return render(self.request, 'experts/qualification_form.html', context={
            "qualification": qualification
        })


class Patients(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "experts/patients.html"

    def test_func(self):
        return self.request.user.groups.filter(name='Expert').exists()

    def get_context_data(self, *args, **kwargs):
        context_data = super(Patients, self).get_context_data(*args, **kwargs)
        context_data["patients"] = Patient.objects.all()
        return context_data


class PatientFilteredView(APIView):
    def get(self, request):
        form_data = dict(request.GET)
        print(form_data)
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response({"patients": serializer.data})