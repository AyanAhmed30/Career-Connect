from pyexpat.errors import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Signup successful! Please log in.")
            return redirect('login')  # Redirect after successful signup
        else:
            messages.error(request, "Please correct the errors below.")  # Optionally show errors
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)

            # Check the role and redirect to the appropriate dashboard
            if user.role == 'company':
                return redirect('company_dashboard')  # Redirect to company dashboard
            elif user.role == 'employee':
                return redirect('employee_dashboard')  # Redirect to employee dashboard
            else:
                messages.error(request, "Role not found. Please contact admin.")
                return redirect('login')  # Fallback redirect to login page

        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('login')  # Redirect back to login page if authentication fails
    
    return render(request, 'accounts/login.html')  # Render login page if GET request
