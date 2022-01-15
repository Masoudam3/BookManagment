import datetime


from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text = "Enter a date between now and four week.")

    def clean_renewal_date(self):
        data = self.cleaned_data["renewal_date"]

        if data < datetime.date.today():
            raise ValidationError(_("Invalid date - Renewal in past."))
        
        if data > datetime.date.today() + datetime.timedelta(weeks = 4):
            raise ValidationError(_("Invalid date - Renewal more than four weeks ahead."))

        return data


class LoginUserForm(forms.Form):
    username = forms.CharField(widget = forms.TextInput(attrs = {"class" : "text", "type" : "text", "name" : "Username", "placeholder" : "Username", "required" : "" }))
    password = forms.CharField(widget = forms.PasswordInput(attrs = {"class" : "text", "type" : "password", "name" : "password", "placeholder" : "Password", "required" : "" }))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        
        if username and password:
            user = authenticate(username = username, password = password)
        
            if not user :
                raise ValidationError("User Does not exist")
        
            if not password :
                raise ValidationError("Incorrect password")
        
        return super(LoginUserForm, self).clean(*args, **kwargs)
                
    
class CreteUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class" : "text",
            "type" : "text",
            "name" : "Username",
            "placeholder" : "Username",
            "required" : ""
        })
        self.fields["email"].widget.attrs.update({
            "class" : "text email",
            "type" : "email",
            "name" : "email",
            "placeholder" : "Email",
            "required" : ""
        })
        self.fields["password1"].widget.attrs.update({
            "class" : "text",
            "type" : "password",
            "name" : "password",
            "placeholder" : "Password",
            "required" : ""
        })
        self.fields["password2"].widget.attrs.update({
            "class" : "text w3lpass",
            "type" : "password",
            "name" : "password",
            "placeholder" : "w3lpass Password",
            "required" : ""
        })
    def clean(self, *args, **kwargs):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1 != password2 :
            raise ValidationError("Your password are not same")
            
        return super(CreteUserForm, self).clean(*args, **kwargs)        
    
    class Meta:
        model = User
        fields =["username", "email", "password1", "password2"]   