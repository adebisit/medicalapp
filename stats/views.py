from django.shortcuts import render
from django.views.generic import TemplateView
from patients.models import Patient, History, Diet
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, When, F, Q, Value, CharField, Count
from datetime import date
from pprint import pprint
# Create your views here.


class Home(LoginRequiredMixin, TemplateView):
    template_name = "stats/home.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super(Home, self).get_context_data(*args, **kwargs)
        context_data.update(**get_context_data())
        return context_data


def get_context_data():
    context_data = {}
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

    age_group = Case(
        When(dob__gte=min_date1, dob__lte=max_date1, then=Value("0 - 4 yrs")),
        When(dob__gte=min_date2, dob__lte=max_date2, then=Value("4 - 12 yrs")),
        When(dob__gte=min_date3, dob__lte=max_date3, then=Value("13 - 19 yrs")),
        When(dob__gte=min_date4, dob__lte=max_date4, then=Value("20 - 35 yrs")),
        When(dob__gte=min_date5, dob__lte=max_date5, then=Value("36 - 50 yrs")),
        When(dob__gte=min_date6, dob__lte=max_date6, then=Value("50 - 70 yrs")),
        default=Value("Above 70 yrs"),
        output_field=CharField()
    )
  
    weight_status = Case(
        When(bmi__lt=18.5, bmi__gte=0, then=Value("Under Weight")),
        When(bmi__lt=25, bmi__gte=18.5, then=Value("Normal Weight")),
        When(bmi__lt=30, bmi__gte=25, then=Value("Over Weight")),
        When(bmi__lt=35, bmi__gte=30, then=Value("Obesity Class 1")),
        When(bmi__lt=40, bmi__gte=35, then=Value("Obesity Class 2")),
        When(bmi__gte=40, then=Value("Extreme Obesity Class 3")),
        default=None,
        output_field=CharField()
    )

    bmi = F('weight') / (F("height") * F("height"))

    patients = Patient.objects.annotate(age_group=age_group, bmi=bmi).annotate(weight_status=weight_status)

    age_groups = patients.values("age_group").annotate(Count('age_group'))
    age_dict = {
        "0 - 4 yrs": 0,
        "4 -12 yrs": 0,
        "13 - 19 yrs": 0,
        "20 - 35 yrs": 0,
        "36 - 50 yrs": 0,
        "50 - 70 yrs": 0,
        "Above 70 yrs": 0
    }
    for age_group in age_groups:
        age_dict[age_group["age_group"]] = age_group["age_group__count"]
    print(age_dict)
    context_data["age_dict"] = age_dict

    weight_status_groups = patients.values("weight_status").annotate(Count('weight_status'))
    weight_status_dict = {
        "Underweight": 0,
        "Normal weight": 0,
        "Overweight": 0,
        "Obesity Class 1": 0,
        "Obesity Class 2": 0,
        "Extreme Obesity Class 3": 0
    }
    for weight_status_group in weight_status_groups:
        weight_status_dict[weight_status_group["weight_status"]] = weight_status_group["weight_status__count"]
    print(weight_status_dict)
    context_data["weight_status_dict"] = weight_status_dict

    blood_groups = patients.values("blood_group").annotate(Count('blood_group')).values("blood_group", "blood_group__count")
    blood_groups_dict = { "A+": 0,"A-": 0, "B+": 0, "B-": 0, "O+": 0, "O-": 0, "AB+": 0, "AB-": 0 }
    for blood_group in blood_groups:
        blood_groups_dict[blood_group["blood_group"].upper()] = blood_group["blood_group__count"]
    print(blood_groups_dict)

    context_data["blood_groups_dict"] = blood_groups_dict

    blood_group_matching = {}
    for blood_group in blood_groups:
        blood_type = blood_group["blood_group"]
        matched_blood_types = []
        if blood_type == "a+":
            matched_blood_types = ["o+", "o-", "a+", "a-"]
        elif blood_type == "a-":
            matched_blood_types = ["o-", "a-"]
        elif blood_type == "b+":
            matched_blood_types = ["o+", "o-", "b+", "b-"]
        elif blood_type == "b-":
            matched_blood_types = ["o-", "b-"]
        elif blood_type == "o+":
            matched_blood_types = ["o-", "o+"]
        elif blood_type == "o-":
            matched_blood_types = ["o-"]
        elif blood_type == "ab+":
            matched_blood_types = ["a+", "a-", "b+", "b-", "o+", "o-", "ab+", "ab-"]
        elif blood_type == "ab-":
            matched_blood_types = ["o-", "a-", "b-", "ab-"]
        blood_match_sum = sum(blood_groups_dict.get(blood.upper(), 0) for blood in matched_blood_types)

        blood_group_matching[blood_type.replace("+", "plus").replace("-", "minus")] = round(blood_match_sum / patients.count() * 100)
    pprint(blood_group_matching)
    context_data["blood_group_matching"] = blood_group_matching
    
    genotypes = patients.values("genotype").annotate(Count('genotype')).values("genotype", "genotype__count")
    genotypes_dict = {
        "AA": 0,
        "AS": 0,
        "AC": 0,
        "SS": 0
    }
    for genotype in genotypes:
        genotypes_dict[genotype["genotype"].upper()] = genotype["genotype__count"]
    print(genotypes_dict)
    context_data["genotypes_dict"] = genotypes_dict

    genotype_matching = {}
    for genotype in genotypes:
        genotype = genotype["genotype"]
        matched_genotypes = []
        if genotype == "aa":
            matched_genotypes = ["aa", "as", "ss", "ac"]
        elif genotype == "as" or genotype == "ac" or genotype == "ss":
            matched_genotypes = ["aa"]
        elif genotype == "ss":
            matched_genotypes = ["aa"]
        genotype_match_sum = sum(genotypes_dict.get(gtype.upper(), 0) for gtype in matched_genotypes)

        genotype_matching[genotype] = round(genotype_match_sum / patients.count() * 100)

        # genotype_matching[genotype["genotype"]] = genotype["genotype__count"]
    pprint(genotype_matching)
    context_data["genotype_matching"] = genotype_matching

    common_diseases = {
        "malaria": "",
        "cholera": "",
        "typhoid": "",
        "coronavirus": ""
    }
    
    for disease in common_diseases:
        common_diseases[disease] = round(History.objects.filter(diagnosis__contains=disease).values("patient").distinct().count() / patients.count() * 100, 2)
    print(common_diseases)
    context_data["common_diseases"] = common_diseases
    return context_data
