from django import forms
from django.contrib.auth import password_validation
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'role', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        # Check if passwords match
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        
        # Optional: Additional password validation
        if password:
            password_validation.validate_password(password)  # Django's built-in password validation

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Set the password for the user (it will be hashed)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
        return user
