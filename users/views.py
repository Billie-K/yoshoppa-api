from django.shortcuts import render, redirect
from django.core.mail import send_mail , BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.models import User 
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .forms import NewUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm

# Create your views here.
def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard:dash_index')
    form = NewUserForm()
    return render(request=request, template_name='registration/register.html', context={"register_form":form})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard:dash_index")
    form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html", context={"login_form":form})

def logout_request(request):
    """A logout for users"""
    logout(request)
    return redirect('users:login')

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form":password_reset_form})
