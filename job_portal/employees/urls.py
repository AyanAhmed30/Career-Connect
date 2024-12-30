from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static


urlpatterns = [
        path('dashboard/', views.employee_dashboard, name='employee_dashboard'),  # This is the correct path for employee dashboard

    path('find_job/', views.find_job, name='find_job'),
    path('logout/', views.logout_employee, name='logout'),
    path('about_job/', views.about_job, name='about_job'),  
    path('apply/<int:job_id>/', views.applied_job, name='applied_job'),
    path('applied_jobs/', views.applied_jobs_list, name='applied_jobs_list'),  # Add this route
      path('interview/<int:application_id>/', views.interview_details, name='interview_details'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
