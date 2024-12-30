from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from companies.models import Job
from .models import AppliedJob
from .models import Job, AppliedJob  # Assuming Job and JobApplication are defined in your models
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import AppliedJob
from companies.models import Job
from django.contrib.auth.decorators import login_required
from .forms import AppliedJobForm
from django.db.models import Q
from accounts.models import CustomUser


@login_required
def find_job(request):
    # Fetch the search query from the GET request
    search_query = request.GET.get('search_query', '')  # Default to an empty string if no search term is provided

    # Fetch all jobs, filtered by the search query if provided
    if search_query:
        jobs = Job.objects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(required_skills__icontains=search_query) |
            Q(qualifications__icontains=search_query) |
            Q(company__username__icontains=search_query)
        )
    else:
        jobs = Job.objects.all()

    # Get the IDs of jobs the user has already applied for
    applied_job_ids = AppliedJob.objects.filter(user=request.user).values_list('job_id', flat=True)

    if request.method == "POST":
        job_id = request.POST.get('job_id')
        resume = request.FILES.get('resume')

        if not resume:
            messages.error(request, "Please upload a resume before applying.")
            return redirect('find_job')

        job = get_object_or_404(Job, id=job_id)

        # Create the AppliedJob instance
        AppliedJob.objects.create(
            user=request.user,
            job=job,
            resume=resume,
            status="Applied",
        )
        messages.success(request, "You have successfully applied for the job!")
        return redirect('find_job')  # Refresh the page to update the status

    return render(request, 'employees/find_job.html', {
        'jobs': jobs,
        'applied_job_ids': applied_job_ids,  # Pass the applied job IDs to the template
        'search_query': search_query,  # Pass the search query to the template
    })
@login_required
def applied_job(request, job_id):
    job = Job.objects.get(id=job_id)

    if request.method == 'POST':
        form = AppliedJobForm(request.POST, request.FILES)

        if form.is_valid():
            applied_job = form.save(commit=False)
            applied_job.user = request.user  # Associate the logged-in user
            applied_job.job = job  # Associate the selected job
            applied_job.status = 'Pending'  # Set the status
            applied_job.save()

            messages.success(request, 'You have successfully applied for the job!')
            return redirect('employees:find_job')

    else:
        form = AppliedJobForm()

    context = {
        'job': job,
        'form': form
    }
    return render(request, 'employees/applied_jobs.html', context)


@login_required
def applied_job(request, job_id):
    job = Job.objects.get(id=job_id)  # Get the job being applied for
    
    if request.method == 'POST':
        form = AppliedJobForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Create the AppliedJob instance and associate it with the user
            applied_job = form.save(commit=False)
            applied_job.user = request.user  # Associate the current logged-in user
            applied_job.job = job  # Associate the selected job
            applied_job.status = 'Pending'  # Set status to Pending
            applied_job.save()  # Save the application

            # Add a success message
            messages.success(request, 'You have successfully applied for the job!')

            return redirect('employees:find_job')  # Redirect to the find job page

    else:
        form = AppliedJobForm()

    context = {
        'job': job,
        'form': form
    }
    return render(request, 'employees/applied_jobs.html', context)


def logout_employee(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

def employee_dashboard(request):
    return render(request, 'employees/dashboard.html')

def about_job(request):
    # Fetch all users with the 'company' role
    companies = CustomUser.objects.filter(role='company')  # Get all companies (users with role 'company')
    
    # Pass the companies to the template
    return render(request, 'employees/about_job.html', {'companies': companies})

@login_required
def applied_jobs_list(request):
    # Fetch applied jobs for the logged-in user
    applied_jobs = AppliedJob.objects.filter(user=request.user)  # This will include all applications including rejected ones
    
    return render(request, 'employees/applied_jobs.html', {
        'applied_jobs': applied_jobs,
    })
@login_required
def interview_details(request, application_id):
    # Get the specific application using its ID
    application = get_object_or_404(AppliedJob, id=application_id)

    # Ensure that the status is "Interview"
    if application.status != 'Interview':
        messages.error(request, "This application does not have an interview scheduled.")
        return redirect('applied_jobs_list')

    return render(request, 'employees/interview_details.html', {'application': application})
