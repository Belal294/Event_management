from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from users.forms import CustomRegistrationForm, SignupForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            participant_group = Group.objects.get(name='Participant')
            user.groups.add(participant_group)  
            return redirect('sign-in')  
    return render(request, 'registration/register.html', {"form": form})


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Your Username & Password is Invalid!")
            print("Faild Login")  
            
    return render(request, 'registration/login.html')


def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    


def signup_view(request):
    if request.method=="POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("login")
        
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form":form})






def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'users/admin_dashboard.html')

