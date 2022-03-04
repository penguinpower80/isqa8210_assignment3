from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from tech.models import User, UserTypes


class ProfileForm(UserChangeForm):
    email = forms.EmailField(label="Email address", required=True, help_text="Required.",)
    phone = forms.CharField(label="Phone", required=True, help_text="Required. Format: ###-###-####",)
    street1 = forms.CharField(label="Street Address 1", required=True, help_text="Required.",)
    street2 = forms.CharField(label="Street Address 2",required=False)
    city = forms.CharField(help_text="Required.")
    state = forms.CharField(help_text="Required.")
    zip = forms.CharField(help_text="Required.")

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        del self.fields['password']

    class Meta:
        model = User
        fields = ("first_name", "last_name","email", "phone", "street1", "street2", "city", "state", "zip",)

    def clean_email(self):
        if User.objects.filter(email="email").exists():
            raise forms.ValidationError("Email is not unique.")
        return self.cleaned_data["email"].lower()

    def clean_phone(self):
        if len(self.cleaned_data["phone"]) != 12:
            raise forms.ValidationError("Please use required phone format.")
        return self.cleaned_data["phone"]


