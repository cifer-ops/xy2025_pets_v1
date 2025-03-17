#coding:utf-8
from django import forms
from accounts.models import UserProfile
import re
import sys
import os

#Login form
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required","id":"user","name":"username"}),
                              max_length=100,error_messages={"required": "username cannot be empty",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required","id":"password","name":"password"}),
                              max_length=200,error_messages={"required": "password cannot be empty",})

#Registration form
class RegForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                              max_length=50,error_messages={"required": "The username cannot be empty",})
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email", "required": "required",}),
                              max_length=50,error_messages={"required": "The email cannot be empty",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                              max_length=20,error_messages={"required": "Password cannot be empty",})
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm password", "required": "required",}),
                              max_length=20,error_messages={"required": "Confirm password cannot be empty",})

    def clean(self):
        if not self.is_valid():
             raise forms.ValidationError('All items are required')
        elif self.cleaned_data['confirm_password'] != self.cleaned_data['password']:
            raise forms.ValidationError('The password is inconsistent when entering the two times')
        else:
            cleaned_data = super(RegForm,self).clean()
        username = self.cleaned_data['username']
        is_email_exist = UserProfile.objects.filter(email=username).exists()
        is_username_exist = UserProfile.objects.filter(username=username).exists()
        if is_username_exist or is_email_exist:
            raise forms.ValidationError(u"This account has been registered")

        return cleaned_data

#Registration form
class RegPhoneForm(forms.Form):
    # username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "username", "required": "required",}),
    #                           max_length=50,error_messages={"required": "Username cannot be empty",})
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Mobile phone", "required": "required",}),
                              max_length=50,error_messages={"required": "The phone cannot be empty",})
    # email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email", }),
    #                          max_length=50, )
    # password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "password", "required": "required",}),
    #                           max_length=20,error_messages={"required": "Password cannot be empty",})
    # confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password", "required": "required",}),
    #                           max_length=20,error_messages={"required": "Confirm password cannot be empty",})

    def clean(self):
        if not self.is_valid():
             raise forms.ValidationError('All items are required')
        else:
            cleaned_data = super(RegPhoneForm,self).clean()
        phone = self.cleaned_data['phone']
        is_mobile_exist = UserProfile.objects.filter(mobile=phone).exists()
        if is_mobile_exist:
            raise forms.ValidationError(u"This mobile phone number has been registered")
        p2 = r'^0\d{2,3}\d{7,8}$|^1[3578]\d{9}$|^147\d{8}'
        phonematch = re.findall(r'^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}', phone)
        if len(phonematch) == 0 or phonematch==None or phonematch=="" :
            raise forms.ValidationError(u"The phone number is incorrect")
        return cleaned_data


