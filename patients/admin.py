from django.contrib import admin
from .models import Patient, History, Diet

# Register your models here.

class DietInline(admin.TabularInline):
    model = Diet

class HistoryInline(admin.TabularInline):
    model = History


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'gender', 'get_age', 'get_bmi', 'get_weight_status')
    inlines = [DietInline, HistoryInline]


@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
    pass

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    pass