from django.shortcuts import render
from django.shortcuts import redirect
from soccer.utils import send_activation_email
from soccer.forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        pass
        # return redirect('soccer_home')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False 
            user.save()
            send_activation_email(request, user) 
            return render(request, "registration/register_done.html", {"email": user.email})
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})

def home(request):
    if not request.user.is_authenticated:
        return redirect('register')
    return render(request, "soccer/home.html", {"user": request.user})

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "activation/activation_success.html")
    else:
        return render(request, "activation/activation_invalid.html")