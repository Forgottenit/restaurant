from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm


def is_staffteam_or_admin(user):
    return user.groups.filter(name='StaffTeam').exists() or user.is_superuser


def send_email_view(request):
    print("Sending email...")

    try:
        send_mail(
            'Test Subject',
            'Test message',
            'ourrestaurantproject2@gmail.com',  # sender email
            ['forgottenit2@gmail.com'],  # recipient email(s)
            fail_silently=False,
        )
        print("Email sent successfully.")
        return JsonResponse({"status": "Email sent successfully"})
    except Exception as e:
        print(str(e))
        return JsonResponse({"status": "Email sending failed."})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully. You are now logged in.')
            return redirect('reservations')
        else:
            messages.error(request, 'There was a problem creating your account. Please check the form and try again.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'You are now logged in.')

            if is_staffteam_or_admin(request.user):
                return redirect('staff_menu')
            else:
                return redirect('reservations')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')