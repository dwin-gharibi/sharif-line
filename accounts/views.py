from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django import forms


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'نام کاربری خود را وارد کنید'})
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'رمز عبور خود را وارد کنید'})
    )

    error_messages = {
        'invalid_login': 'نام کاربری یا رمز عبور اشتباه است.',
        'inactive': 'این حساب کاربری غیرفعال است.',
    }


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='رمز عبور',
        help_text="""رمز عبور شما باید:
        - حداقل ۸ کاراکتر باشد
        - نباید خیلی رایج باشد
        - نباید فقط عدد باشد
        - نباید مشابه اطلاعات شخصی شما باشد""",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'رمز عبور خود را وارد کنید'})
    )
    password2 = forms.CharField(
        label='تکرار رمز عبور',
        help_text='برای تایید، همان رمز عبور قبلی را وارد کنید.',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'رمز عبور خود را تکرار کنید'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': 'نام کاربری',
        }
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'نام کاربری خود را وارد کنید'}),
        }

    error_messages = {
        'password_mismatch': 'رمزهای عبور وارد شده یکسان نیستند.',
    }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']
        labels = {
            'bio': 'درباره من',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'درباره خود بنویسید...'}),
        }



class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    form_class = CustomAuthenticationForm


class CustomLogoutView(LogoutView):
    next_page = 'home'


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'accounts/profile_update.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('profile')
