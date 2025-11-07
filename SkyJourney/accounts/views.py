from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User

# importing custom forms
from .forms import CustomLoginForm, CustomRegisterForm

# --- Login and Register Views ---
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = CustomLoginForm

class CustomRegisterView(CreateView):
    form_class = CustomRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('signin')  # Redirect to login page after successful registration


# --- Password Reset Flow ---

import random
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailOTP

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            otp = generate_otp()
            EmailOTP.objects.create(email=email, otp=otp)

            subject = "Your OTP Code"
            message = f"Your OTP is: {otp}\nThis code will expire in 10 minutes."
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

            # Redirect to OTP verification with email in session
            request.session['email_for_reset'] = email
            return redirect('verify-otp')

    return render(request, 'accounts/pwd_reset/send_otp_email.html')

# verifying the otp unless expired.

from django.contrib.auth.models import User
from .models import EmailOTP

def verify_otp(request):
    context = {}
    email = request.session.get('email_for_reset')

    if not email:
        return redirect('send-otp')  # safeguard

    if request.method == 'POST':
        otp_input = request.POST.get('otp')

        try:
            otp_record = EmailOTP.objects.filter(email=email, otp=otp_input).latest('created_at')
            if otp_record.is_expired():
                context['error'] = "OTP expired. Try again."
            else:
                # OTP is valid → redirect to password reset form with user info in session
                request.session['verified_email'] = email
                return redirect('set-new-password')
        except EmailOTP.DoesNotExist:
            context['error'] = "Invalid OTP. Try again."

    return render(request, 'accounts/pwd_reset/verify_otp.html', context)

# setting new password taking the verified email from session

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User

def set_new_password(request):
    email = request.session.get('verified_email')
    if not email:
        return redirect('send-otp')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            # Clean session
            request.session.pop('verified_email', None)
            request.session.pop('email_for_reset', None)
            return render(request, 'accounts/pwd_reset/done.html')
    else:
        form = SetPasswordForm(user)

    return render(request, 'accounts/pwd_reset/set_new_password.html', {'form': form})
