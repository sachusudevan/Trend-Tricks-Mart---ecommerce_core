from django import forms
from apps.users.models import Users



class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['email','password']


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = [  'username', 
    		        'password', 
    		        'email', 
    		        'first_name', 
    		        'last_name'
                ]