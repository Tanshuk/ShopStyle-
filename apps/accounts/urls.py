from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # ── Core Auth ──────────────────────────────────────
    path('login/',    views.login_view,    name='login'),
    path('logout/',   views.logout_view,   name='logout'),
    path('register/', views.register_view, name='register'),

    # ── Profile ────────────────────────────────────────
    path('profile/',         views.profile_view,      name='profile'),
    path('profile/edit/',    views.edit_profile_view,  name='edit_profile'),
    path('password/change/', views.change_password_view, name='change_password'),

    # ── Password Reset (4-step Django flow) ────────────
    path('password/reset/',
         views.CustomPasswordResetView.as_view(),
         name='password_reset'),

    path('password/reset/done/',
         views.CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),

    path('password/reset/confirm/<uidb64>/<token>/',
         views.CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('password/reset/complete/',
         views.CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]