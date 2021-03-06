from django.shortcuts import render
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token import account_activation_token
from django.utils.encoding import force_bytes, force_text
from .models import User
from django.contrib.auth.models import Group
from experts.models import Expert
from patients.models import Patient
from django.shortcuts import redirect, reverse
# Create your views here.


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            group = form.cleaned_data["group"]
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            
            subject = "MediStats - Activate your Account"
            message = render

            mail_args = {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                "group": group
            }

            html_message = render_to_string('accounts/activation_email.html', mail_args)
            message = render_to_string('accounts/activation_email.txt', mail_args)
            user.email_user(subject, message, None, html_message=html_message)
            return render(request, 'accounts/confirm_activation.html', context={'email': user.email})
    else:
        form = SignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def activate(request, uidb64, token, group):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        if group == "user":
            patient_group, created = Group.objects.get_or_create(name='Patient')
            user.groups.add(patient_group)
            Patient.objects.create(user=user)
        elif group == "expert":
            expert_group, created = Group.objects.get_or_create(name='Expert')
            user.groups.add(expert_group)
            Expert.objects.create(user=user)
        return render(request, 'accounts/confirmation-success.html')
    else:
        return render(request, 'accounts/confirmation-fail.html')


def login_success(request):
    if request.user.groups.filter(name='Expert').exists():
        return redirect("experts:home")
    else:
        return redirect("patients:home")