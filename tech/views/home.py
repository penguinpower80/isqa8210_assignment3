import logging

from django.shortcuts import render

# Create your views here.
from tech.models import Job


def home(request):
    user = request.user
    if user.is_anonymous:
        return render(request, 'tech/home.html')
    if request.user.is_tech():
        jobs = Job.objects.filter(technician_id=user.id)
    else:
        jobs = Job.objects.all()

    return render(request, 'tech/home.html',{
        'jobCollection': jobs
    })