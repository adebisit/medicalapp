from django.db import models
from accounts.models import User
from django.urls import reverse_lazy, reverse
import os
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
# Create your models here.


def get_file_type(name):
    ext = os.path.splitext(name)[1]
    if ext.lower() in [".jpg", ".png"]:
        return "image"
    elif ext.lower() == ".pdf":
        return "pdf"
    elif ext.lower() == ".docx":
        return "docx"
    else:
        return False


def validate_file_extension(value):
    file_type = get_file_type(value.name)
    if not file_type:
        raise ValidationError(_('Unsupported file extension.'))


class Expert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"{self.user.get_full_name()}"

    def is_verified(self):
        unverified = any(qualification.status in ('pending', 'unverified') for qualification in self.qualifications.all())
        return not unverified


class Qualification(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name="qualifications")
    title = models.CharField(max_length=225)
    date_issued = models.DateField()
    validity_period = models.DurationField(null=True, blank=True)
    issued_by = models.CharField(max_length=225)
    STATUS_CHOICES = (
        ('verified', "Verified"),
        ('pending', "Pending Verification"),
        ('unverified', "Unverified")
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def get_absolute_url(self):
        return reverse("experts:qualification_view", args=[self.id,])


class Document(models.Model):
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE, related_name="proofs")
    document = models.FileField(validators=[validate_file_extension])

    def get_file_type(self):
        print(get_file_type(self.document.name))
        return get_file_type(self.document.name)

