import logging

from django.shortcuts import render, redirect
from django.urls import reverse

from tech.forms.newrequest import NewRequestForm
from tech.helpers.helpers import getRedirectWithParam

def request(request):
    context = {}
    form = NewRequestForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            newrequest = form.save(commit=False)
            newrequest.customer = request.user
            newrequest.save()
            return getRedirectWithParam(1)
        else:
            return render(request, 'tech/request.html', {'form': form})
    else:
        context['form'] = form
        return render(request, 'tech/request.html', context)
