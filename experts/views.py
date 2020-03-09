from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404
from .models import Expert, Qualification
from patients.models import Patient
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PatientSerializer
from datetime import date
from django.db.models import Case, When, F, Q, Value, CharField
from functools import reduce
import operator
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

        age_groups = form_data.get("age-group[]")
        blood_groups = form_data.get("age-group[]")
        genotypes = form_data.get("genotype[]")
        histories = form_data.get("medical-history[]")
        weight_statuses = form_data.get("weight-status[]")

        age_filter = Q(age_group__in=age_groups) if age_groups else Q()
        blood_group_filter = Q(blood_group__in=blood_groups) if blood_groups else Q()
        genotype_filter = Q(genotype__in=genotypes) if genotypes else Q()
        history_filter = reduce(operator.or_, (Q(histories__diagnosis__icontains=history) | Q(histories__description__icontains=history) for history in histories)) if histories else Q()
        weight_status_filter = Q(weight_status__in=weight_statuses) if weight_statuses else Q()

        current = date.today()
    
        min_date1 = date(current.year - 4, current.month, current.day)
        max_date1 = date(current.year, current.month, current.day)

        min_date2 = date(current.year - 12, current.month, current.day)
        max_date2 = date(current.year - 4, current.month, current.day)

        min_date3 = date(current.year - 19, current.month, current.day)
        max_date3 = date(current.year - 13, current.month, current.day)

        min_date4 = date(current.year - 35, current.month, current.day)
        max_date4 = date(current.year - 20, current.month, current.day)

        min_date5 = date(current.year - 50, current.month, current.day)
        max_date5 = date(current.year - 36, current.month, current.day)

        min_date6 = date(current.year - 70, current.month, current.day)
        max_date6 = date(current.year - 51, current.month, current.day)

        age_group_annotate = Case(
            When(dob__gte=min_date1, dob__lte=max_date1, then=Value("babies")),
            When(dob__gte=min_date2, dob__lte=max_date2, then=Value("childre")),
            When(dob__gte=min_date3, dob__lte=max_date3, then=Value("teenagers")),
            When(dob__gte=min_date4, dob__lte=max_date4, then=Value("youths")),
            When(dob__gte=min_date5, dob__lte=max_date5, then=Value("adults")),
            When(dob__gte=min_date6, dob__lte=max_date6, then=Value("elders")),
            default=Value("old"),
            output_field=CharField()
        )
    
        weight_status_annotate = Case(
            When(bmi__lt=18.5, bmi__gte=0, then=Value("under-weight")),
            When(bmi__lt=25, bmi__gte=18.5, then=Value("normal-weight")),
            When(bmi__lt=30, bmi__gte=25, then=Value("overweight")),
            When(bmi__lt=35, bmi__gte=30, then=Value("obesity-class-1")),
            When(bmi__lt=40, bmi__gte=35, then=Value("obesity-class-2")),
            When(bmi__gte=40, then=Value("extreme-obesity-class-3")),
            default=None,
            output_field=CharField()
        )

        bmi = F('weight') / (F("height") * F("height"))

        patients = Patient.objects.annotate(age_group=age_group_annotate, bmi=bmi).annotate(weight_status=weight_status_annotate)

        patients = patients.filter(age_filter | blood_group_filter | genotype_filter | history_filter | weight_status_filter).distinct()
        
        serializer = PatientSerializer(patients, many=True)
        return Response({"patients": serializer.data})