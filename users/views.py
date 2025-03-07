from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from django.contrib.auth import login, authenticate, logout
from users.forms import CustomRegistrationForm, SignupForm, AssignRoleForm, CreateGroupForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from events.models import Event
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from users.forms import CustomUserCreationForm, CustomRegistrationForm, AssignRoleForm, CreateGroupForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm, EditProfileForm
from django.views.generic import TemplateView, UpdateView


# def sign_up(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('dashboard')  
#     else:
#         form = CustomUserCreationForm()
    
#     return render(request, "registration/register.html", {"form": form})



def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard_redirect')  
            
        else:
            messages.error(request, "Your Username & Password is Invalid!")
            print("Failed Login")  
            
    return render(request, 'registration/login.html')



def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)  
        if form.is_valid():
            User = get_user_model()
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])

            # Set a default value for 'role' if it's not provided in the form
            user.role = 'default_role'  # Set a default role (adjust as needed)

            user.save()
            return redirect("login")
        
    else:
        form = SignupForm()
    
    return render(request, "registration/signup.html", {"form": form})

def is_admin(user):
    return user.groups.filter(name='Admin').exists()


@user_passes_test(is_admin)
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()
    events = Event.objects.all()
    
    profile_picture = None
    if request.user.is_authenticated:
        profile_picture = request.user.profile_picture if hasattr(request.user, 'profile_picture') else None

    return render(request, 'admin/dashboard.html', {
        "users": users,
        "events": events,
        "profile_picture": profile_picture
    })


# def assing_role(request, user_id):
#     user = get_object_or_404(User, id=user_id)
#     form = AssignRoleForm()

#     if request.method == 'POST':
#         form = AssignRoleForm(request.POST)  
#         if form.is_valid():
#             role = form.cleaned_data.get('role')  
            
#             user.groups.clear()
#             user.groups.add(role)
            
#             messages.success(request, f"User {user.username} has been assigned to the {role.name} role.")
            
#             return redirect('admin-dashboard')  
    
#     return render(request, 'admin/assign_role.html', {'form': form, 'user': user})



def assing_role(request, user_id):
    user = get_object_or_404(User, id=user_id)  
    form = AssignRoleForm()
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)  
        if form.is_valid():
            role = form.cleaned_data.get('role')  
            user.groups.clear()
            user.groups.add(role)  
            messages.success(request, f"User {user.username} has been assigned to the {role.name} role.")
            return redirect('admin-dashboard')  
    return render(request, 'admin/assign_role.html', {'form': form, 'user': user})


class CreateGroupView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Group
    form_class = CreateGroupForm
    template_name = "admin/create_group.html"
    success_url = reverse_lazy("create-group")

    def test_func(self):
        return self.request.user.groups.filter(name="Admin").exists()

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Group {self.object.name} has been created successfully")
        return response

@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})



@login_required
def dashboard_redirect(request):
    user = request.user

    if user.groups.filter(name='Admin').exists():
        return redirect('/users/admin/dashboard/') 
    elif user.groups.filter(name='Organizer').exists():
        return redirect('/users/dashboard/organizer/')  
    else:
        return redirect('/users/dashboard/participant/')  


@login_required
def organizer_dashboard(request):
    return render(request, 'admin/organizer_dashboard.html')

@login_required
def participant_dashboard(request):
    return render(request, 'admin/participant_dashboard.html')





User = get_user_model()

def activate_user(request, user_id, token):
    user = get_object_or_404(User, id=user_id)

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=['is_active'])
        messages.success(request, "Your account has been activated successfully! You can now log in.")
        return redirect("login")  
    else:
        messages.error(request, "Invalid activation link or token expired.")
        return redirect("home") 

# class ChangePassword(PasswordChangeView):
#     template_name = 'accounts/password_change.html'
#     form_class = CustomPasswordChangeForm

class ChangePassword(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been successfully updated!')
        return super().form_valid(form)

    def form_invalid(self, form):
        
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)




class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()

        context['profile_picture'] = user.profile_picture.url if user.profile_picture else None

        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login

        return context


class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('profile')


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('login')
    html_email_template_name = 'registration/reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context

    def form_valid(self, form):
        email = form.cleaned_data.get("email")

        if not User.objects.filter(email=email).exists():
            messages.error(self.request, "This email address is not registered.")
            return redirect('password_reset')

        messages.success(self.request, 'A reset email has been sent. Please check your email.')
        return super().form_valid(form)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(
            self.request, 'Password reset successfully')
        return super().form_valid(form)
