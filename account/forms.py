from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'full_name')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('full_name', 'profile_picture', 'phone_number')

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'phone_number', 'profile_picture']

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(max_length=254)

class PasswordResetConfirmForm(forms.Form):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm New Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data