from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_http_methods,require_GET
import uuid

from .forms import (
    CustomUserCreationForm, 
    UserProfileUpdateForm, 
    PasswordResetRequestForm,
    PasswordResetConfirmForm,
    AccountDeleteForm
)
from .models import CustomUser


@require_http_methods(request_method_list=['GET','POST'])
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('user_panel')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/register.html', {'form': form})


@require_http_methods(request_method_list=['GET','POST'])
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('user_panel')
        else:
            messages.error(request, 'Invalid login credentials')
    return render(request, 'account/login.html')


@login_required
@require_GET
def user_panel(request):
    return render(request, 'account/user_panel.html')


@login_required
@require_http_methods(request_method_list=['GET','POST'])
def profile_update(request):
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_panel')
    else:
        form = UserProfileUpdateForm(instance=request.user)
    return render(request, 'account/profile_update.html', {'form': form})

@login_required
@require_http_methods(request_method_list=['GET','POST'])
def password_reset_request(request):
    reset_link=None
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                reset_token = str(uuid.uuid4())
                reset_link = f"http://{request.get_host()}/password-reset-confirm/{reset_token}/"
                user.token = reset_token
                user.save()
                # if you dont have an email still you can access to reset_pass link on the reset_pass page
                # just click on send email and then use reset_link button
                # and comment send_mail section
                send_mail(
                    'Password Reset Request',
                    f'Click the link to reset your password: {reset_link}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Password reset link sent to your email')
            except CustomUser.DoesNotExist:
                messages.error(request, 'No user found with this email')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'account/password_reset_request.html', {'form': form,'reset_link':reset_link})


@require_http_methods(request_method_list=['GET','POST'])
def password_reset_confirm(request, token):
    user = CustomUser.objects.filter(id=request.user.id)
    if user.exists():
        user = user.first()
        if request.method == 'POST' and user.token==token:
            form = PasswordResetConfirmForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password1']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password reset successful')
                return redirect('login')
        else:
            form = PasswordResetConfirmForm()
        return render(request, 'account/password_reset_confirm.html', {'form': form})

    messages.error(request, 'No user found with this email or invalid token')

@require_GET
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')


@login_required
@require_http_methods(request_method_list=['GET','POST'])
def account_delete_view(request):
    if request.method == 'POST':
        form = AccountDeleteForm(request.POST)
        if form.is_valid():
            # Verify current password
            if request.user.check_password(form.cleaned_data['confirm_password']):
                request.user.delete()
                messages.success(request, 'Your account has been permanently deleted.')
                return redirect('register')
            else:
                messages.error(request, 'Incorrect password')
    else:
        form = AccountDeleteForm()
    return render(request, 'account/account_delete.html', {'form': form})