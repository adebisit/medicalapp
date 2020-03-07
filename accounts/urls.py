from django.urls import path
from django.urls import path, re_path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/success/', views.login_success, name='login_success'),
    path("logout/", auth_views.LogoutView.as_view(), {'template_name': 'logged_out.html'}, name="logout"),
    path('signup/', views.signup, name="signup"),
    path(r'activate/<uidb64>[0-9A-Za-z_\-]+/<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}/<group>', views.activate, name='activate'),
]