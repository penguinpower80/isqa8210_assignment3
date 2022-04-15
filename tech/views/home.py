import logging

from django.db.models import Q
from django.shortcuts import render

from tech.helpers.helpers import getMessageText
from tech.models import Job, JobStatus


def home(request):
    user = request.user
    if user.is_anonymous:
        return render(request, 'tech/home.html')

    if request.GET.get('msg'):
        msg = getMessageText( int(request.GET.get('msg')) )
    else:
        msg = ''

    phrase_filter = None

    if request.user.is_tech():
        jobs = Job.objects.filter(technician_id=user.id)
    else:
        jobs = Job.objects.filter(customer_id=user.id)

    status_filter = request.GET.get('status')
    if status_filter:
        jobs = jobs.filter(status=status_filter.upper())
    level_filter = request.GET.get('level')
    if level_filter:
        jobs = jobs.filter(level=level_filter.upper())
    phrase_filter = request.GET.get('phrase')
    if phrase_filter:
        jobs = jobs.filter(Q(description__icontains=phrase_filter))
    jobs = jobs.order_by('-created_at')

    return render(request, 'tech/home.html', {
        'jobCollection': jobs,
        'search_phrase': phrase_filter,
        'message': msg
    })
