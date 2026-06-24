"""
All authentication and profile forms for the accounts app.
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.core.exceptions import ValidationError

User = get_user_model()


# ─────────────────────────────────────────────
# LOGIN FORM
# ─────────────────────────────────────────────
class LoginForm(AuthenticationForm):
    """
    Custom login form using email instead of username.
    Extends Django's built-in AuthenticationForm.
    """
    username = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class':       'form-control form-control-lg',
            'placeholder': 'you@example.com',
            'autofocus':   True,
            'autocomplete':'email',
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class':       'form-control form-control-lg',
            'placeholder': 'Enter your password',
            'autocomplete':'current-password',
            'id':          'loginPassword',
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        label='Keep me logged in',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the default "username" label text
        self.fields['username'].label = 'Email Address'

    error_messages = {
        'invalid_login': (
            'No account found with this email and password. '
            'Please check your credentials and try again.'
        ),
        'inactive': 'This account has been disabled.',
    }


# ─────────────────────────────────────────────
# REGISTER FORM
# ─────────────────────────────────────────────
class RegisterForm(UserCreationForm):
    """
    Extended registration form — collects first name, last name,
    phone, and email, plus accepts terms and conditions.
    """
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class':       'form-control form-control-lg',
            'placeholder': 'First Name',
            'autocomplete':'given-name',
        })
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class':       'form-control form-control-lg',
            'placeholder': 'Last Name',
            'autocomplete':'family-name',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class':       'form-control form-control-lg',
            'placeholder': 'you@example.com',
            'autocomplete':'email',
        })
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class':       'form-control form-control-lg',
            'placeholder': '10-digit mobile number',
            'autocomplete':'tel',
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class':       'form-control form-control-lg',
            'placeholder': 'Create a strong password',
            'autocomplete':'new-password',
            'id':          'regPassword',
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class':       'form-control form-control-lg',
            'placeholder': 'Repeat your password',
            'autocomplete':'new-password',
        })
    )
    terms = forms.BooleanField(
        required=True,
        label='I agree to the Terms & Conditions and Privacy Policy',
        error_messages={'required': 'You must accept the terms and conditions.'},
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model  = User
        fields = (
            'first_name', 'last_name',
            'email', 'phone',
            'password1', 'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                'An account with this email already exists. '
                'Try logging in instead.'
            )
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if phone:
            # Remove common separators
            digits = phone.replace(' ', '').replace('-', '').replace('+', '')
            if not digits.isdigit():
                raise ValidationError('Phone number must contain only digits.')
            if len(digits) < 10:
                raise ValidationError('Phone number must be at least 10 digits.')
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email      = self.cleaned_data['email'].lower().strip()
        user.first_name = self.cleaned_data['first_name'].strip()
        user.last_name  = self.cleaned_data['last_name'].strip()
        user.phone      = self.cleaned_data.get('phone', '')
        # Auto-generate username from email (required field)
        user.username   = user.email.split('@')[0]
        # Ensure username is unique
        base_username = user.username
        counter = 1
        while User.objects.filter(username=user.username).exists():
            user.username = f'{base_username}{counter}'
            counter += 1

        if commit:
            user.save()
        return user


# ─────────────────────────────────────────────
# EDIT PROFILE FORM
# ─────────────────────────────────────────────
class EditProfileForm(forms.ModelForm):
    """
    Lets users update their personal info and avatar.
    """
    class Meta:
        model  = User
        fields = (
            'first_name', 'last_name',
            'phone', 'date_of_birth', 'avatar',
        )
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Last Name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '10-digit mobile number'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
            'avatar': forms.FileInput(attrs={
                'class':  'form-control',
                'accept': 'image/*',
                'id':     'avatarInput',
            }),
        }
        labels = {
            'date_of_birth': 'Date of Birth',
            'avatar':        'Profile Picture',
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # 2 MB limit
            if avatar.size > 2 * 1024 * 1024:
                raise ValidationError(
                    'Image file too large. Maximum size is 2 MB.'
                )
            # Check file type
            content_type = getattr(avatar, 'content_type', '')
            if not content_type.startswith('image/'):
                raise ValidationError(
                    'Please upload a valid image file (JPEG, PNG, etc.).'
                )
        return avatar


# ─────────────────────────────────────────────
# CUSTOM PASSWORD CHANGE FORM
# ─────────────────────────────────────────────
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Your current password'
        })
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'New password (min 8 chars)'
        })
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Repeat new password'
        })
    )


# ─────────────────────────────────────────────
# CUSTOM PASSWORD RESET FORM
# ─────────────────────────────────────────────
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class':       'form-control form-control-lg',
            'placeholder': 'Enter your registered email',
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()
        if not User.objects.filter(email=email, is_active=True).exists():
            # We don't reveal whether the email exists (security best practice)
            # Just return the email — Django will silently skip sending
            pass
        return email


# ─────────────────────────────────────────────
# CUSTOM SET PASSWORD FORM (after reset link)
# ─────────────────────────────────────────────
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Create your new password',
        })
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Repeat your new password',
        })
    )