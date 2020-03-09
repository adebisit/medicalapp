from django.db import models
from accounts.models import User
# Create your models here.
from uuid import uuid4
from datetime import date
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


def no_future(value):
    today = date.today()

    if value > today:
        raise ValidationError(_("Date of Birth cannot be in the future"))


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    patient_id = models.UUIDField(default=uuid4, editable=False)
    
    dob = models.DateField(verbose_name="Date of Birth", null=True, blank=True,  validators=[no_future,])

    BLOOD_GROUP_CHOICES = (
        ('a+', "A+"),
        ("a-", "A-"),
        ('b+', "B+"),
        ('b-', "B-"),
        ('o-', "O-"),
        ('o+', "O+"),
        ('ab-', "AB-"),
        ('ab+', "AB+")
    )

    blood_group = models.CharField(choices=BLOOD_GROUP_CHOICES, max_length=3, null=True, blank=True)
    GENOTYPE_CHOICES = (
        ('aa', "AA"),
        ('as', "AS"),
        ('SS', "SS"),
        ('ac', "AC"),
    )
    genotype = models.CharField(choices=GENOTYPE_CHOICES, max_length=3, null=True, blank=True)

    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(1),])
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(1),])

    GENDER_CHOICES = (
        ('male', "Male"),
        ('female', "Female")
    )
    gender = models.CharField(choices=GENDER_CHOICES, max_length=63, null=True, blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def get_name(self):
        return self.user.first_name + " " + self.user.last_name
    
    def get_age(self):
        if self.dob:
            today = date.today()
            return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return None

    def get_bmi(self):
        if self.height is None or self.weight is None:
            return None
        return round(self.weight/(self.height * self.height), 1)

    def get_weight_status(self):
        bmi = self.get_bmi()
        if bmi is None:
            return None
        
        status = ""
        if bmi < 18.5:
            status = "Under weight"
        elif 18.5 <= bmi < 25:
            status = "Normal weight"
        elif 25 <= bmi < 30:
            status = "Overweight"
        elif 30 <= bmi < 35:
            status = "Obesity Class 1"
        elif 35 <= bmi < 40:
            status = "Obesity Class 2"
        else:
            status = "Extreme Obesity Class 3"
        return status

    def get_absolute_url(self):
        return reverse("patients:home")

    def get_patient_view_url(self):
        return reverse("patients:patient-home", args=[self.pk, ])


    # frequency of excercising
    
        

class History(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="histories")

    diagnosis = models.CharField(max_length=255)
    description = models.TextField()
    correction = models.TextField()
    date_occured = models.DateField()

    def __str__(self):
        return self.diagnosis

    
class Diet(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name="diets")
    
    carbs = models.DecimalField(verbose_name="Carbonhydrates", default=15, max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    fats = models.DecimalField(default=15, max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    dietary_fiber = models.DecimalField(verbose_name="Dietary Fibre", default=15, max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    minerals = models.DecimalField(default=15, max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    proteins = models.DecimalField(default=15, max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    vitamins = models.DecimalField(default=15, max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    water = models.DecimalField(default=10, max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])

    frequency = models.PositiveIntegerField(default=1)

    def clean(self, *args, **kwargs):
        print(self.patient)
        # if self.patient.diets.count() > 3:
        #     raise ValidationError(
        #         _("User has a maximum of 4 Diets")
        #     )

        balanced = self.carbs + self.fats + self.dietary_fiber + self.minerals + self.proteins + self.vitamins + self.water
        print(balanced)
        if round(balanced) > 105:
            raise ValidationError(
                _("The percentage of nutrition classes exceeds 100%")
            )
        super(Diet, self).clean(*args, **kwargs)



# class Alergies

