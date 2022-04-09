from django import forms

from tech.models import Job


class NewRequestForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = (
            'description',
            'level',
            'appointment',
        )
        labels = {
            'appointment': 'Desired Appointment Date and Time'
        }