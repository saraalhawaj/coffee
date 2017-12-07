from django import forms
from django.contrib.auth.models import User


class UserSignup(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username','password'] 


		widgets = {

		'password': froms.PasswordInput(),
		}




class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())