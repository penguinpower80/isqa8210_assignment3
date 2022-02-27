from django import forms
from django.contrib.auth.forms import UserCreationForm

from tech.models import User, UserTypes


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label="Username", required=True, help_text="Required.",)
    email = forms.EmailField(label="Email address", required=True, help_text="Required.",)
    phone = forms.CharField(label="Phone", required=True, help_text="Required. Format: ###-###-####",)
    street1 = forms.CharField(label="Street Address 1", required=True, help_text="Required.",)
    street2 = forms.CharField(label="Street Address 2",required=False)
    city = forms.CharField(help_text="Required.")
    state = forms.CharField(help_text="Required.")
    zip = forms.CharField(help_text="Required.")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name","email", "phone", "street1", "street2", "city", "state", "zip", "password1", "password2")

    def clean_username(self):
        if User.objects.filter(username="username").exists():
            raise forms.ValidationError("Username is not unique.")
        return self.cleaned_data["username"].lower()

    def clean_email(self):
        if User.objects.filter(email="email").exists():
            raise forms.ValidationError("Email is not unique.")
        return self.cleaned_data["email"].lower()

    def clean_phone(self):
        if len(self.cleaned_data["phone"]) != 12:
            raise forms.ValidationError("Please use required phone format.")
        return self.cleaned_data["phone"]

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = (self.cleaned_data["username"])
        user.email = (self.cleaned_data["email"])
        user.set_password(self.cleaned_data["password1"])
        user.type = UserTypes.CUSTOMER #FORCE THEM TO BE A CUSTOMER!
        if commit:
            user.save()
        return user
