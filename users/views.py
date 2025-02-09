from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from users.forms import CustomRegistrationForm, SignupForm
from django.contrib.auth import login

def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sign-in')
            
        else:
            print("Form is not valid")
    return render(request, 'registration/register.html', {"form": form})


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Doc", username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html')


def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')
    


def signup_view(request):
    if request.method=="POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("sign-in")
        
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form":form})

