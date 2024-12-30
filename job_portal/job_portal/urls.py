from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from accounts.views import signup_view  # Import the signup view directly


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  
    path('employees/', include('employees.urls')),
    path('companies/', include('companies.urls')),  # Include URLs for companies app

]
if settings.DEBUG:  # Serve media files only in development mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)