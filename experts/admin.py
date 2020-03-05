from django.contrib import admin
from .models import Expert, Qualification, Document

# Register your models here.

class QualificationInline(admin.TabularInline):
    model = Qualification

class DocumentInline(admin.TabularInline):
    model = Document

@admin.register(Expert)
class ExpertModel(admin.ModelAdmin):
    inlines = [QualificationInline,]

@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    inlines = [DocumentInline,]

