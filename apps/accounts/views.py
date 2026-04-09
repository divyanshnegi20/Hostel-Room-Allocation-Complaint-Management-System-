from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, CustomLoginForm, ProfileUpdateForm


def register_view(request):
    """Student registration."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Your account has been created successfully.')
            return redirect('dashboard:home')
    else:
        form = StudentRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'dashboard:home')
            return redirect(next_url)
    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """User logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """View and edit user profile."""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})
