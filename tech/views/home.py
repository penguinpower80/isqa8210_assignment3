import logging

from django.shortcuts import render

# Create your views here.
from tech.models import Job, JobStatus


def home(request):
    user = request.user
    if user.is_anonymous:
        return render(request, 'tech/home.html')
    if request.user.is_tech():
        jobs = Job.objects.filter(technician_id=user.id)
        status_filter = request.GET.get('status')
        if status_filter:
            jobs = jobs.filter(status=status_filter.upper() )
        jobs = jobs.order_by('created_at')
    else:
        jobs = Job.objects.all()

    return render(request, 'tech/home.html',{
        'jobCollection': jobs
    })