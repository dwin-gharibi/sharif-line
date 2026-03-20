from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('surveys/', include('surveys.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('faq/',TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('terms/', TemplateView.as_view(template_name='terms.html'), name='terms'),
    path('login/', accounts_views.CustomLoginView.as_view(), name='login'),
    path('signup/', accounts_views.SignUpView.as_view(), name='signup'),
    path('logout/', accounts_views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', accounts_views.ProfileView.as_view(), name='profile'),
    path('profile/update/', accounts_views.ProfileUpdateView.as_view(), name='profile_update'),
    path('password-change/', accounts_views.PasswordChangeView.as_view(), name='password_change'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
