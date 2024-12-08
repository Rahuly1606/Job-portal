from django.urls import path
from . import views
from .views import Applicant_dashboard, upload_resume, view_applied_jobs, saved_jobs_view, save_job, remove_saved_job, \
    cancel_application
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('applicant_dashboard/', Applicant_dashboard, name='Applicant_dashboard'),
    path('applicant_signup/', views.applicant_signup, name='applicant_signup'),
    path('applicant_login/', views.applicant_login, name='applicant_login'),
    path('applicant_logout/', views.applicant_logout, name='applicant_logout'),
    path('resume/', views.resume, name='resume'),
    path('upload-resume/', upload_resume, name='upload_resume'),
    path('applied_jobs/', view_applied_jobs, name='view_applied_jobs'),
    path('Alljobs/',views.Alljobs,name='Alljobs'),
    path('saved-jobs/', saved_jobs_view, name='saved_jobs'),
    path('save-job/<int:job_id>/', save_job, name='save_job'),
    path('remove-saved-job/<int:saved_job_id>/', remove_saved_job, name='remove_saved_job'),
    path('cancel-application/<int:application_id>/', cancel_application, name='cancel_application'),
    path('additional_details/', views.additional_details, name='additional_details'),
]
