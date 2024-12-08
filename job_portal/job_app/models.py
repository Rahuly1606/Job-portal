from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.


class contact(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    address = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name

from django.db import models
from django.conf import settings

class Job(models.Model):
    company_name = models.CharField(max_length=100, null=True, blank=True)
    founded_date = models.DateField(null=True, blank=True)
    company_location = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50, choices=[
        ('Remote', 'Remote'),
        ('Onsite', 'Onsite'),
        ('Hybrid', 'Hybrid')
    ])
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    requirements = models.TextField()
    ideal_candidate = models.TextField(default='N/A')
    availability = models.BooleanField(default=True)
    vacancy_seats = models.IntegerField(default=0)  # Maximum number of positions
    filled_vacancies = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    applicants = models.ManyToManyField('Applicant.Applicant', related_name='applied_jobs', blank=True)

    def __str__(self):
        return self.title




class sign_up(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)


