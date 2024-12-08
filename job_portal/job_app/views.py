from audioop import reverse

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView
from .models import contact as ContactModel
from datetime import datetime
from django.contrib import messages
from django.utils import timezone

from django.shortcuts import render

from Applicant.models import Application

from .forms import ApplicationStatusForm


def job_list1(request):
    jobs = Job.objects.all()
    keyword = request.GET.get('job-keyword')
    location = request.GET.get('location')
    job_type = request.GET.get('job-type')
    industry = request.GET.get('industry')

    if keyword:
        jobs = jobs.filter(title__icontains=keyword)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if job_type:
        jobs = jobs.filter(job_type__iexact=job_type)
    if industry:
        jobs = jobs.filter(industry__iexact=industry)

    return render(request, 'home.html', {'jobs': jobs})


@login_required
def add_job_view(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name'),
        founded_date = request.POST.get('founded_date')
        company_location = request.POST.get('company_location'),
        title = request.POST.get('title')
        industry = request.POST.get('industry')
        job_type = request.POST.get('job_type')
        location = request.POST.get('location')
        salary = request.POST.get('salary')
        vacancy_seats = request.POST.get('vacancy_seats')
        requirements = request.POST.get('requirements')
        ideal_candidate = request.POST.get('ideal_candidate')
        availability = 'availability' in request.POST

        new_job = Job(
            company_name=company_name,
            founded_date=founded_date,
            company_location=company_location,
            title=title,
            industry=industry,
            job_type=job_type,
            location=location,
            salary=salary,
            vacancy_seats=vacancy_seats,
            requirements=requirements,
            ideal_candidate=ideal_candidate,
            availability=availability,
            user=request.user  # Save the user who added the job
        )
        new_job.save()
        messages.success(request, "New Job added.")
        return redirect('Managejobs')

    return render(request, 'Addjob.html')


@login_required
def update_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, user=request.user)  # Ensure the user can only update their own jobs

    if request.method == 'POST':
        job.company_name = request.POST['company_name']
        job.founded_date = request.POST['founded_date']
        job.company_location = request.POST['company_location']
        job.title = request.POST['title']
        job.industry = request.POST['industry']
        job.job_type = request.POST['job_type']
        job.salary = request.POST['salary']
        job.requirements = request.POST['requirements']
        job.ideal_candidate = request.POST['ideal_candidate']
        job.availability = 'availability' in request.POST
        job.save()
        messages.success(request, "Job updated successfully.")
        return redirect('Managejobs')

    return render(request, 'Addjob.html', {'job': job})


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, user=request.user)  # Ensure user can only delete their own jobs
    job.delete()
    messages.add_message(request, messages.INFO, "Job deleted successfully.", extra_tags='manage_jobs')
    return redirect('Managejobs')


# from django.shortcuts import render
from .models import Job

from Applicant.models import Applicant, Resume, SavedJob


def home(request):
    jobs = Job.objects.order_by('-created_at')[:9]

    # Get the applicant ID from the session
    applicant_id = request.session.get('applicant_id')
    applicant_username = None
    recruiter_username = None

    # If the applicant is logged in, get their username
    if applicant_id:
        try:
            applicant = Applicant.objects.get(id=applicant_id)
            applicant_username = applicant.username
        except Applicant.DoesNotExist:
            applicant_username = None

    # If the recruiter is logged in, get their username
    if request.user.is_authenticated and not applicant_id:
        recruiter_username = request.user.username

    return render(request, 'home.html', {
        'jobs': jobs,
        'applicant_username': applicant_username,
        'recruiter_username': recruiter_username  # Pass recruiter username to the template
    })


def job_detail(request, job_id):
    jobs = Job.objects.all()
    job = get_object_or_404(Job, id=job_id)
    applicant_id = request.session.get('applicant_id')
    applicant_username = None
    recruiter_username = None
    has_resume = False
    has_applied = False
    is_applicant = False
    has_saved = False
    is_available = job.availability and job.vacancy_seats > job.application_set.count()  # Check if job is available

    if applicant_id:
        try:
            applicant = Applicant.objects.get(id=applicant_id)
            has_resume = Resume.objects.filter(applicant=applicant).exists()
            has_applied = Application.objects.filter(applicant_id=applicant_id, job=job).exists()
            has_saved = SavedJob.objects.filter(applicant=applicant, job=job).exists()
            applicant_username = applicant.username
            is_applicant = True
        except Applicant.DoesNotExist:
            applicant_username = None
            has_resume = False

    if request.user.is_authenticated and not applicant_id:
        recruiter_username = request.user.username
    recommended_jobs = Job.objects.exclude(application__applicant_id=applicant_id).exclude(id=job_id)
    return render(request, 'ViewDetails.html', {
        'job': job,
        'jobs': recommended_jobs,
        'applicant_username': applicant_username,
        'recruiter_username': recruiter_username,
        'has_resume': has_resume,
        'has_applied': has_applied,
        'is_applicant': is_applicant,
        'has_saved': has_saved,
        'is_available': is_available,  # Pass availability status to the template
        'request': request
    })




def index(request):
    if request.user.is_authenticated:
        jobs = Job.objects.filter(user=request.user).order_by('-created_at')

        # Count total jobs for the recruiter
        total_jobs = jobs.count()

        # Count total applicants for the recruiter's jobs
        total_applicants = Application.objects.filter(job__user=request.user).count()

        # Count total active jobs for the recruiter
        total_active_jobs = jobs.filter(availability=True).count()
    else:
        jobs = Job.objects.none()
        total_jobs = 0
        total_applicants = 0
        total_active_jobs = 0

    return render(request, 'index.html', {
        'jobs': jobs,
        'total_jobs': total_jobs,
        'total_applicants': total_applicants,
        'total_active_jobs': total_active_jobs
    })


def loginsignup(request):
    return render(request, 'loginsignup.html')


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        address = request.POST.get('address')

        new_contact = ContactModel(name=name, age=age, email=email, address=address, date=datetime.today())
        new_contact.save()
        messages.success(request, "Profile details updated.")

    return render(request, 'contact.html')


class ManageJobsView(LoginRequiredMixin, View):  # Ensure the user is logged in
    def get(self, request):
        # Filter jobs by the currently logged-in user
        jobs = Job.objects.filter(user=request.user)

        # Prepare job data with remaining vacancies
        job_data = []
        for job in jobs:
            remaining_vacancies = job.vacancy_seats - job.application_set.count()
            job_data.append({
                'job': job,
                'remaining_vacancies': remaining_vacancies
            })

        return render(request, 'Managejobs.html', {'jobs': job_data})


def apply_for_job(request, job_id):
    # Check if the applicant is logged in by session
    applicant_id = request.session.get('applicant_id')
    if not applicant_id:
        return redirect('applicant_login')
    job = get_object_or_404(Job, id=job_id)
    applicant = get_object_or_404(Applicant, id=applicant_id)
    existing_application = Application.objects.filter(job=job, applicant=applicant).exists()
    if not existing_application:
        Application.objects.create(job=job, applicant=applicant, applied_at=timezone.now())
    return redirect('Applicant_dashboard')


def job_applicants(request, job_id):
    # Get the job object
    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        application_id = request.POST.get("application_id")
        status = request.POST.get("status")
        interview_time = request.POST.get("interview_time")

        # Get the application object
        try:
            application = Application.objects.get(id=application_id, job_id=job_id)
        except Application.DoesNotExist:
            messages.error(request, "Application not found.")
            return redirect(reverse('job_applicants', args=[job_id]))

        # Update the status
        if status:
            application.status = status
            application.save()
            messages.success(request, "Status updated successfully.")

        # Schedule interview if interview_time is provided
        if interview_time:
            application.interview_time = interview_time
            application.save()
            messages.success(request, "Interview scheduled successfully.")

    # Retrieve all applications for the job
    applications = Application.objects.filter(job_id=job_id)
    return render(request, 'job_applicants.html', {
        'job': job,
        'applications': applications,
    })


def job_listk(request):
    if request.user.is_authenticated:
        # Get all jobs for the authenticated user
        jobs = Job.objects.filter(user=request.user).order_by('-created_at')

        # Count total jobs for the recruiter
        total_jobs = jobs.count()

        # Count total applicants for the recruiter's jobs
        total_applicants = Application.objects.filter(job__user=request.user).count()

        # Count total active jobs for the recruiter
        total_active_jobs = jobs.filter(availability=True).count()

        # Get the keyword from the search form
        keyword = request.GET.get('query')  # Ensure this matches your form input name

        # Filter jobs based on the search parameters
        if keyword:
            jobs = jobs.filter(title__icontains=keyword)

    else:
        jobs = Job.objects.none()  # No jobs if not authenticated
        total_jobs = 0
        total_applicants = 0
        total_active_jobs = 0

    return render(request, 'index.html', {
        'jobs': jobs,
        'total_jobs': total_jobs,
        'total_applicants': total_applicants,
        'total_active_jobs': total_active_jobs
    })


from django.http import JsonResponse


class UpdateVacancyView(View):
    def post(self, request, job_id):
        import json
        data = json.loads(request.body)
        new_vacancy = data.get('total_vacancy')

        try:
            job = Job.objects.get(id=job_id)
            job.vacancy_seats = new_vacancy
            job.save()
            return JsonResponse({'message': 'Vacancy updated successfully!'})
        except Job.DoesNotExist:
            return JsonResponse({'message': 'Job not found!'}, status=404)


def aboutus(request):
    return render(request,'AboutUs.html')
