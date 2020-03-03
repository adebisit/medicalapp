from django.urls import path
from . import views

app_name = "patients"

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('edit/', views.PatientEdit.as_view(), name="patient_edit"),
    path("history/add", views.HistoryAdd.as_view(), name="history_add"),
    path("histories/<pk>/edit", views.HistoryEdit.as_view(), name="history_edit"),
    path("diets/add", views.DietAdd.as_view(), name="history_add"),
    path("diets/<pk>/edit", views.DietEdit.as_view(), name="history_edit"),
    path("diets/<pk>/delete", views.DietDelete.as_view(), name="history_delete"),
]