from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
] 