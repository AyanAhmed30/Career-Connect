from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from employees.models import AppliedJob
from .models import Job
from employees.models import AppliedJob
from django.db.models import Count
from datetime import datetime, timedelta
from django.db.models.functions import TruncDate
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Job
from .models import Job
from .forms import JobForm
from django.contrib.auth.decorators import login_required
from .models import Job
from employees.models import AppliedJob




# Company Dashboard View
@login_required
def company_dashboard(request):
    # Check if the logged-in user is a company
    if request.user.is_authenticated and request.user.role == 'company':
        company_name = request.user.username  # Assuming the company's name is the username
        return render(request, 'companies/dashboard.html', {'company_name': company_name})
    else:
        return redirect('login')  
    
    
    
    
    
    
    

@login_required
def post_job(request):
    if request.user.role != 'company':
        return redirect('login')
    
    if request.method == 'POST':
        title = request.POST['job_title']
        description = request.POST['job_description']
        required_skills = request.POST.get('required_skills', '')
        experience = request.POST.get('experience', '')
        qualifications = request.POST.get('qualifications', '')
        age = request.POST.get('age', None)

        Job.objects.create(
            title=title,
            description=description,
            company=request.user,
            required_skills=required_skills,
            experience=experience,
            qualifications=qualifications,
            age=age,
        )
        return redirect('company_dashboard')

    return render(request, 'companies/post_job.html')# Applications View


@login_required
def applications(request):
    if request.user.role == 'company':  # Ensure only companies can see applications
        # Fetch all jobs posted by the company
        jobs = Job.objects.filter(company=request.user)
        
        # Fetch all applications for those jobs that are not rejected or scheduled for an interview
        applications = AppliedJob.objects.filter(job__in=jobs).exclude(status__in=['Rejected', 'Interview'])

        return render(request, 'companies/applications.html', {'applications': applications})
    else:
        return redirect('login')  # Redirect if the user is not a company

    
@login_required
def manage_application(request, application_id):
    application = get_object_or_404(AppliedJob, id=application_id)

    if request.method == 'POST':
        if 'delete' in request.POST:
            # Update status to Rejected
            application.status = 'Rejected'
            application.save()
            messages.success(request, "Application has been rejected.")
            return redirect('applications')

        elif 'send_interview' in request.POST:
            # Get interview details from form input
            interview_date = request.POST.get('interview_date')
            interview_time = request.POST.get('interview_time')
            interview_location = request.POST.get('interview_location')

            # Update application with interview details and change status to Interview
            application.interview_date = interview_date
            application.interview_time = interview_time
            application.interview_location = interview_location
            application.status = 'Interview'  # Change status to Interview
            application.save()

            messages.success(request, "Interview details have been sent.")
            return redirect('applications')

    return render(request, 'companies/manage_application.html', {'application': application})
def logout_company(request):
    logout(request)  # Log out the current user
    return redirect('signup')  # Redirect to the signup page after logging out
@login_required
def company_jobs(request):
    # Fetch jobs posted by the logged-in company (user)
    jobs = Job.objects.filter(company=request.user)

    if request.method == 'POST':
        # Handle editing of the job
        if 'edit' in request.POST:
            job_id = request.POST.get('job_id')
            job = get_object_or_404(Job, id=job_id, company=request.user)
            job.title = request.POST.get('job_title', job.title)
            job.description = request.POST.get('job_description', job.description)
            job.required_skills = request.POST.get('required_skills', job.required_skills)
            job.experience = request.POST.get('experience', job.experience)
            job.qualifications = request.POST.get('qualifications', job.qualifications)
            job.age = request.POST.get('age', job.age)
            job.save()
            messages.success(request, 'Job updated successfully!')

        # Handle deletion of the job
        elif 'delete' in request.POST:
            job_id = request.POST.get('job_id')
            job = get_object_or_404(Job, id=job_id, company=request.user)
            job.delete()
            messages.success(request, 'Job deleted successfully!')

        return redirect('company_jobs')

    return render(request, 'companies/company_jobs.html', {'jobs': jobs})
@login_required
def edit_job(request, job_id):
    # Check if the logged-in user is a company
    if request.user.role != 'company':
        return redirect('login')  # Redirect to login page if the user is not a company

    try:
        job = Job.objects.get(id=job_id, company=request.user)
    except Job.DoesNotExist:
        messages.error(request, 'Job not found or you do not have permission to edit this job.')
        return redirect('company_jobs')

    # Handle form submission for editing the job
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('company_jobs')
    else:
        form = JobForm(instance=job)

    return render(request, 'companies/edit_job.html', {'form': form, 'job': job})
def delete_job(request, job_id):
    # Ensure the user is logged in and is a company
    if not request.user.is_authenticated or request.user.role != 'company':
        return redirect('login')
    
    # Get the job object by ID, or return a 404 if not found
    job = get_object_or_404(Job, id=job_id)
    
    # Make sure the job belongs to the logged-in company
    if job.company != request.user:
        messages.error(request, "You do not have permission to delete this job.")
        return redirect('company_jobs')
    
    # Delete the job and redirect
    job.delete()
    messages.success(request, "Job deleted successfully.")
    return redirect('company_jobs')

