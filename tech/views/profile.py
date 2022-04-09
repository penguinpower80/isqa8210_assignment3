import logging

from django.contrib.auth import login
from django.shortcuts import render, redirect

from tech.forms import RegistrationForm
from tech.forms.profile import ProfileForm
from tech.helpers.helpers import getRedirectWithParam


def profile(request):
    context = {}

    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            return getRedirectWithParam(2)
        else:
            return render(request, 'tech/profile.html', {'form': form})
    else:
        context['form'] = form
        return render(request, 'tech/profile.html', context)