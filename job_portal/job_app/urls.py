from django.urls import path
from . import views
from .views import add_job_view, update_job, ManageJobsView, delete_job, job_list1, job_applicants, \
    apply_for_job, job_listk, UpdateVacancyView

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('job-list1/', job_list1, name='job_list1'),
    path('job-listk/', job_listk, name='job_listk'),
    path('loginsignup/', views.loginsignup, name='loginsignup'),
    path('manage-jobs/', ManageJobsView.as_view(), name='Managejobs'),
    path('update-job/<int:job_id>/', update_job, name='update_job'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('delete_job/<int:job_id>/', delete_job, name='delete_job'),
    path('contact/', views.contact_view, name='contact'),
    path('addjob/', views.add_job_view, name='Addjob'),
    path('job/<int:job_id>/applicants/', job_applicants, name='job_applicants'),
    path('apply/<int:job_id>/', apply_for_job, name='apply_for_job'),
    path('update_vacancy/<int:job_id>/', UpdateVacancyView.as_view(), name='update_vacancy'),
    path('aboutus/',views.aboutus,name='AboutUs'),
]

