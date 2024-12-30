from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/', views.company_dashboard, name='company_dashboard'),
    path('post_job/', views.post_job, name='post_job'),
    path('applications/', views.applications, name='applications'),
    path('logout/', views.logout_company, name='logout_company'),
   path('manage_application/<int:application_id>/', views.manage_application, name='manage_application'),    path('company/jobs/', views.company_jobs, name='company_jobs'),  # Page to display company jobs
    path('company/jobs/delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('company/jobs/edit/<int:job_id>/', views.edit_job, name='edit_job'),  # URL to edit a job
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
