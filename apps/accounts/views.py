"""
Complete authentication views for the accounts app.
Uses Django's built-in auth machinery + custom forms.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import (
    authenticate, login, logout,
    get_user_model, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import (
    LoginForm,
    RegisterForm,
    EditProfileForm,
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
)

User = get_user_model()


# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
def login_view(request):
    """
    Login with email and password.
    Redirects authenticated users away from this page.
    """
    if request.user.is_authenticated:
        return redirect('core:home')

    form = LoginForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user         = form.get_user()
            remember_me  = form.cleaned_data.get('remember_me', False)

            login(request, user)

            # Session expiry: browser session vs 30 days
            if not remember_me:
                request.session.set_expiry(0)   # expires on browser close
            else:
                request.session.set_expiry(86400 * 30)  # 30 days

            messages.success(
                request,
                f'Welcome back, {user.get_short_name()}! 👋'
            )

            # Redirect to ?next= param if present, else home
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect('core:home')

        else:
            messages.error(
                request,
                'Invalid email or password. Please try again.'
            )

    context = {
        'form':       form,
        'page_title': 'Login',
        'next':       request.GET.get('next', ''),
    }
    return render(request, 'accounts/login.html', context)


# ─────────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────────
def logout_view(request):
    """POST-only logout (CSRF protection)."""
    user_name = request.user.get_short_name() if request.user.is_authenticated else ''
    logout(request)
    messages.success(request, f'You have been logged out. See you soon, {user_name}! 👋')
    return redirect('core:home')


# ─────────────────────────────────────────────
# REGISTER
# ─────────────────────────────────────────────
def register_view(request):
    """
    User registration.
    Automatically logs in after successful registration.
    """
    if request.user.is_authenticated:
        return redirect('core:home')

    form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            # Auto-login after registration
            login(
                request, user,
                backend='apps.accounts.backends.EmailBackend'
            )
            messages.success(
                request,
                f'Welcome to ShopStyle, {user.first_name}! '
                f'Your account has been created successfully. 🎉'
            )
            return redirect('core:home')
        else:
            messages.error(
                request,
                'Please fix the errors below and try again.'
            )

    context = {
        'form':       form,
        'page_title': 'Create Account',
    }
    return render(request, 'accounts/register.html', context)


# ─────────────────────────────────────────────
# PROFILE
# ─────────────────────────────────────────────
@login_required
def profile_view(request):
    """User profile page — shows orders, wishlist count, info."""
    user = request.user
    context = {
        'page_title':    'My Profile',
        'user':          user,
        # order_count and wishlist_count added in later steps
        'order_count':   0,
        'wishlist_count': 0,
    }
    return render(request, 'accounts/profile.html', context)


# ─────────────────────────────────────────────
# EDIT PROFILE
# ─────────────────────────────────────────────
@login_required
def edit_profile_view(request):
    """Edit name, phone, DOB, avatar."""
    form = EditProfileForm(
        request.POST  or None,
        request.FILES or None,
        instance=request.user,
    )

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully. ✅')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please fix the errors below.')

    context = {
        'form':       form,
        'page_title': 'Edit Profile',
    }
    return render(request, 'accounts/edit_profile.html', context)


# ─────────────────────────────────────────────
# CHANGE PASSWORD
# ─────────────────────────────────────────────
@login_required
def change_password_view(request):
    """Change password while logged in."""
    form = CustomPasswordChangeForm(request.user, request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            # Keep the user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(
                request,
                'Your password has been changed successfully. 🔒'
            )
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please fix the errors below.')

    context = {
        'form':       form,
        'page_title': 'Change Password',
    }
    return render(request, 'accounts/change_password.html', context)


# ─────────────────────────────────────────────
# PASSWORD RESET (Django built-in CBVs + our templates + custom forms)
# ─────────────────────────────────────────────
class CustomPasswordResetView(PasswordResetView):
    """Step 1: user enters email → Django sends reset link."""
    template_name      = 'accounts/password_reset.html'
    form_class         = CustomPasswordResetForm
    success_url        = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/emails/password_reset_email.html'
    subject_template_name = 'accounts/emails/password_reset_subject.txt'
    extra_context      = {'page_title': 'Forgot Password'}


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Step 2: confirmation that email was sent."""
    template_name = 'accounts/password_reset_done.html'
    extra_context = {'page_title': 'Check Your Email'}


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Step 3: user clicks link and sets new password."""
    template_name = 'accounts/password_reset_confirm.html'
    form_class    = CustomSetPasswordForm
    success_url   = reverse_lazy('accounts:password_reset_complete')
    extra_context = {'page_title': 'Set New Password'}


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Step 4: success page after password was reset."""
    template_name = 'accounts/password_reset_complete.html'
    extra_context = {'page_title': 'Password Reset Complete'}