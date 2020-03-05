from django.urls import path
from . import views

app_name = "experts"

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('patients', views.Patients.as_view(), name="patients"),
    path('qualifications/<pk>', views.QualificationView.as_view(), name="qualification_view"),
    path('qualifications/<pk>/edit', views.QualificationEdit.as_view(), name="qualification_edit"),
]