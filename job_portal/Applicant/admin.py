from django.contrib import admin
from .models import Applicant, Resume, Application, Applicant_detail

admin.site.register(Applicant)

admin.site.register(Resume)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

admin.site.register(Application)
admin.site.register(Applicant_detail)