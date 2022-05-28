from django.conf import settings
from django.forms import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from apps.accounts.models import ThemeConfiguration
from apps.users.models import Users
import logging
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMessage
from django.template.loader import render_to_string



logger = logging.getLogger(__name__)




def themeConfiguration(request):
    if request.user.is_authenticated:
        print(request.POST.get('status',0))
        theme = get_object_or_404(ThemeConfiguration, user_id=request.user.id)
        theme.theme = request.POST.get('status',0)
        theme.save()
        return JsonResponse({"status" : True})
    return JsonResponse({"status" : False})


class AccountSettingsView(View):
    def __init__(self):
        self.context = {}
        self.template = 'account/settings.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template,self.context)

    def post(self, request, *args, **kwargs):

        action_type = request.POST.get('action_type')

        
        if action_type == '1':
            update_profile = self.updateProfile(request)

        if action_type == '2':
            update_password = self.updatePassword(request)

        return redirect('account:account.settings')

    def updateProfile(self,request):
        username = request.POST.get('username','')
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        email = request.POST.get('email','')
        try:
            data = Users.objects.get(pk=request.user.id)
            
            data.username   = username
            data.first_name = first_name
            data.last_name  = last_name
            data.email      = email
            if request.FILES.__len__() != 0:
                data.image = request.FILES['image']

            data.save()
            messages.success(request, f"Profile Successfully Updated")
            return True
        except Exception as e:
            logger.error('Something went wrong '+str(e))
            messages.error(request, f"Something went wrong")
            return False

    def updatePassword(self, request):
        password = request.POST.get('password').strip()
        new_password = request.POST.get('new-password').strip()
        confirm_new_password = request.POST.get('confirm-new-password').strip()

        try:
            if password and new_password and new_password == confirm_new_password:
                user = request.user
                saveuser = Users.objects.get(id=user.id)
                if user.check_password(password):
                    saveuser.set_password(new_password);
                    saveuser.save()
                    update_session_auth_hash(request, saveuser)
                    messages.success(request, f"Password Successfully Updated")
                    return True
                else:
                    messages.warning(request, f"Incorrect old Password")
                    return False
            else:
                messages.error(request, f"Something went wrong")
                return False

        except Exception as e:
            messages.error(request, f"Something went wrong")
            return False




 


def resendVerificationEmail(request):
    from_email = settings.EMAIL_FROM_ADDREESS
    to_email = ['sachusudeve8690@gmail.com']  
    subject = settings.PROJECT_NAME +'- Verify your email'
    
    body = render_to_string(
        template_name='mail/verify-email.html'
    ).strip()
    
    message = EmailMessage(subject, body, from_email, to_email)
    message.content_subtype = 'html'
    if message.send():
        messages.success(request, "Verification sent to your registered email address.")
    else:  
        messages.error(request, "Somethng went wrong. Please try again.")  
        
    return redirect('account:account.settings')






    