from django import forms
import re
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm, AuthenticationForm, 
    PasswordChangeForm, PasswordResetForm, SetPasswordForm
)
from django.contrib.auth.models import Permission, Group
from .models import CustomUser
from django.contrib.auth import get_user_model


class StyledFormMixin:
    def apply_styling(self):
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styling()


class RegisterForm(StyledFormMixin, UserCreationForm):
    class Meta:
        model = CustomUser  
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class CustomRegistrationForm(StyledFormMixin, forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser  
        fields = ['username', 'first_name', 'last_name', 'password1', 'confirm_password', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []
        if len(password1) < 8:
            errors.append('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', password1):
            errors.append('Password must include at least one uppercase letter.')
        if not re.search(r'[a-z]', password1):
            errors.append('Password must include at least one lowercase letter.')
        if not re.search(r'[0-9]', password1):
            errors.append('Password must include at least one number.')
        if not re.search(r'[@#$%^&+=]', password1):
            errors.append('Password must include at least one special character.')
        if errors:
            raise forms.ValidationError(errors)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


class SignupForm(StyledFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match! Try again.")
        return cleaned_data


class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'bio', 'profile_picture'] 

class AssignRoleForm(StyledFormMixin, forms.Form):
    role = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, widget=forms.Select())


class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label='Assign Permissions'
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']


class CustomPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("new_password1") != cleaned_data.get("new_password2"):
            raise forms.ValidationError("The new passwords do not match.")
        return cleaned_data


class CustomPasswordResetForm(StyledFormMixin, PasswordResetForm):
    pass


class CustomPasswordResetConfirmForm(StyledFormMixin, SetPasswordForm):
    pass


class CustomUserCreationForm(StyledFormMixin, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'profile_picture']


class CustomUserChangeForm(StyledFormMixin, UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'profile_picture']
