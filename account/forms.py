from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .validators import ComplexPasswordValidator, validate_username
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(
        validators=[validate_username],
        help_text="Username must be 4-50 characters, alphanumeric and underscores"
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text='Password must be complex'
    )
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'full_name')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        validator = ComplexPasswordValidator()
        try:
            validator.validate(password)
        except forms.ValidationError as e:
            raise forms.ValidationError(e.messages)
        return password


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
        label="New Password",
        validators=[ComplexPasswordValidator]
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm New Password",
        validators=[ComplexPasswordValidator]
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2