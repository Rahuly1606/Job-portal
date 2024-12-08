from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Resume, Applicant, Application, SavedJob, Applicant_detail
from job_app.models import Job


def applicant_signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'Applicant_signup.html')

        try:
            applicant = Applicant(name=name,username=username, email=email)
            applicant.set_password(password)  # Hash password
            applicant.save()

            messages.success(request, "Applicant account created successfully. You can now log in.")
            return redirect('applicant_login')
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")

    return render(request, 'Applicant_signup.html')


from datetime import datetime, timezone

from datetime import datetime, timezone


def Applicant_dashboard(request):
    applicant_id = request.session.get('applicant_id')
    applied_jobs_count = 0
    interviews_count = 0
    applied_jobs = []
    interviews = []

    if applicant_id:
        try:
            applicant = Applicant.objects.get(id=applicant_id)
            # Get all applications for the applicant
            applied_jobs = Application.objects.filter(applicant=applicant)
            applied_jobs_count = applied_jobs.count()

            # Filter for interviews
            interviews = applied_jobs.filter(status='interview')  # Assuming 'interview' is the status for interviews
            interviews_count = interviews.count()

            # Check if each interview is overdue
            for interview in interviews:
                if interview.interview_time and interview.interview_time < datetime.now(timezone.utc):
                    interview.overdue = True
                    interview.overdue_reference_time = interview.interview_time
                else:
                    interview.overdue = False

            has_resume = Resume.objects.filter(applicant=applicant).exists()
        except Applicant.DoesNotExist:
            applicant = None
            has_resume = False
    else:
        applicant = None
        has_resume = False

    return render(request, 'Applicant_dashboard.html', {
        'applicant': applicant,
        'has_resume': has_resume,
        'applied_jobs_count': applied_jobs_count,
        'interviews_count': interviews_count,
        'applied_jobs': applied_jobs,
        'interviews': interviews,
        'request': request
    })


def applicant_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            applicant = Applicant.objects.get(username=username)

            if applicant.check_password(password):
                request.session['applicant_id'] = applicant.id
                return redirect('Applicant_dashboard')
            else:
                messages.error(request, "Invalid username or password")
        except Applicant.DoesNotExist:
            messages.error(request, "Invalid username or password")

    return render(request, 'Applicant_login.html')


def resume(request):
    resumes = Resume.objects.all()
    return render(request, 'resume.html', {'resumes': resumes})



def upload_resume(request):
    if request.method == 'POST':
        resume_file = request.FILES.get('resume_file')
        recruiter_name = request.POST.get('recruiter_name')
        recruiter_email = request.POST.get('recruiter_email')
        recruiter_position = request.POST.get('recruiter_position')
        applicant_id = request.session.get('applicant_id')

        if resume_file and recruiter_name and recruiter_email and recruiter_position and applicant_id:
            Resume.objects.create(
                applicant_id=applicant_id,
                resume_file=resume_file,
                recruiter_name=recruiter_name,
                recruiter_email=recruiter_email,
                recruiter_position=recruiter_position
            )
            messages.success(request, "Resume uploaded successfully.")
            return redirect('Applicant_dashboard')
        else:
            messages.error(request, "Please provide all required fields and ensure you are logged in.")

    return render(request, 'upload_resume.html')


# views.py
from django.shortcuts import render

from datetime import datetime, timezone

def view_applied_jobs(request):
    applicant_id = request.session.get('applicant_id')  # Get the applicant ID from the session
    if not applicant_id:  # If there's no applicant ID in the session, redirect to login
        return redirect('applicant_login')

    # Retrieve the current logged-in applicant
    applicant = get_object_or_404(Applicant, id=applicant_id)

    # Filter the applications for the current applicant
    applied_jobs = Application.objects.select_related('job').filter(applicant=applicant)

    # Add overdue status and overdue reference time to each application
    for application in applied_jobs:
        if application.interview_time and application.interview_time < datetime.now(timezone.utc):
            application.overdue = True
            application.overdue_reference_time = application.interview_time
        else:
            application.overdue = False

    return render(request, 'view_applied_jobs.html', {'applied_jobs': applied_jobs})

def cancel_application(request, application_id):
    applicant_id = request.session.get('applicant_id')
    if not applicant_id:
        return redirect('applicant_login')

    # Get the application to cancel
    application = get_object_or_404(Application, id=application_id, applicant_id=applicant_id)
    application.delete()  # Remove the application

    messages.success(request, "Job application has been canceled..")
    return redirect('view_applied_jobs')


def applicant_logout(request):
    request.session.flush()  # Clear the session data
    return redirect('Applicant_login')


def Alljobs(request):

    jobs = Job.objects.order_by('-created_at')


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

    jobs = jobs[:9]

    return render(request, 'Alljobs.html', {'jobs': jobs})



def applicant_context(request):
    applicant = None
    if request.session.get('applicant_id'):
        try:
            applicant = Applicant.objects.get(id=request.session['applicant_id'])
        except Applicant.DoesNotExist:
            applicant = None
    return {'applicant': applicant}



def saved_jobs_view(request):
    applicant_id = request.session.get('applicant_id')
    saved_jobs = SavedJob.objects.filter(applicant__id=applicant_id).select_related('job')

    return render(request, 'saved_jobs.html', {'saved_jobs': saved_jobs})

from django.http import JsonResponse, Http404


def save_job(request, job_id):
    if request.method == 'POST':
        applicant_id = request.session.get('applicant_id')
        job = get_object_or_404(Job, id=job_id)
        SavedJob.objects.get_or_create(applicant_id=applicant_id, job=job)
        messages.success(request, f"{job.title} has been saved to your bookmarks.")
        return redirect('job_detail', job_id=job.id)

def remove_saved_job(request, saved_job_id):
    applicant_id = request.session.get('applicant_id')
    saved_job = get_object_or_404(SavedJob, id=saved_job_id, applicant_id=applicant_id)
    saved_job.delete()  # Remove the saved job
    messages.success(request, f"{saved_job.job.title} has been removed from your saved jobs.")
    return redirect('saved_jobs')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Applicant_detail  # Ensure this matches your model name


def additional_details(request):
    # Get applicant ID from session
    applicant_id = request.session.get('applicant_id')
    if not applicant_id:
        messages.error(request, "Session expired. Please log in again.")
        return redirect('applicant_login')

    # Fetch applicant details
    try:
        applicant_detail = get_object_or_404(Applicant_detail, applicant__id=applicant_id)
        applicant = applicant_detail.applicant  # Access the related Applicant
    except Http404:
        messages.error(request, "No details found for this applicant.")
        return redirect('Applicant_dashboard')

    if request.method == 'POST':
        # Update applicant details from POST data
        applicant_detail.phone_number = request.POST.get('phone_number', applicant_detail.phone_number)
        applicant_detail.address = request.POST.get('address', applicant_detail.address)
        applicant_detail.linkedin_profile = request.POST.get('linkedin_profile', applicant_detail.linkedin_profile)
        applicant_detail.current_job_title = request.POST.get('current_job_title', applicant_detail.current_job_title)
        applicant_detail.professional_summary = request.POST.get('professional_summary', applicant_detail.professional_summary)
        applicant_detail.company_name = request.POST.get('company_name', applicant_detail.company_name)
        applicant_detail.degree = request.POST.get('degree', applicant_detail.degree)
        applicant_detail.institution = request.POST.get('institution', applicant_detail.institution)
        applicant_detail.graduation_date = request.POST.get('graduation_date', applicant_detail.graduation_date)
        applicant_detail.languages_known = request.POST.get('languages_known', applicant_detail.languages_known)
        applicant_detail.save()

        # Success message
        messages.success(request, "Your details have been updated successfully.")
        return redirect('Applicant_dashboard')

    # Pass both Applicant and Applicant_detail data to the template
    context = {
        'applicant_detail': applicant_detail,
        'applicant': applicant,  # Include username and email from Applicant
    }
    return render(request, 'Applicant_details.html', context)
