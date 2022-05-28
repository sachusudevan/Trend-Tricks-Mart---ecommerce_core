from django.urls import path, re_path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'accounts'

urlpatterns = [

    path('switch-theme/', login_required(views.themeConfiguration), name='accounts.theme.configuration'),
    path('settings/', login_required(views.AccountSettingsView.as_view()), name='account.settings'),
    path('resend-verification-email/', login_required(views.resendVerificationEmail), name='resend.verification.email')
    
]
