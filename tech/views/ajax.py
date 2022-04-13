import logging
from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_datetime

from tech.helpers.helpers import canAccess
from tech.models import JobPart, Job, Part, PartLocation, JobTime, Technician

'''
List a parts from a job
'''


def jobparts(request, jobid):
    job = get_object_or_404(Job, pk=jobid)
    if not canAccess(request.user, job):
        return HttpResponse(status=401)
    parts = JobPart.objects.filter(job_id=jobid)
    return render(request, 'blocks/job_parts.html', {
        'partsCollection': parts,
        'jobid': jobid
    })


'''
Add a part from a job
'''


def addpart(request, jobid, partid):
    job = get_object_or_404(Job, pk=jobid)
    if not canAccess(request.user, job):
        return HttpResponse(status=401)
    part = Part.objects.get(pk=partid)
    jobpart = JobPart()
    jobpart.job = job
    jobpart.part = part

    status = request.POST.get('status')
    if status:
        jobpart.status = status.upper()
    else:
        jobpart.status = PartLocation.PENDING

    jobpart.cost = part.cost
    jobpart.save()

    return render(request, 'blocks/part_row.html', {
        'part': part,
        'jobpart': jobpart
    })


'''
Remove a part from a job
'''


def removepart(request, jobid, jobpartid):
    job = get_object_or_404(Job, pk=jobid)
    jobpart = get_object_or_404(JobPart, pk=jobpartid)
    if not canAccess(request.user, job):
        return HttpResponse(status=401)

    jobpart.delete()
    return HttpResponse(status=200)


'''
Update a job part element
'''


def updatejobpart(request, jobid, jobpartid):
    job = get_object_or_404(Job, pk=jobid)
    jobpart = get_object_or_404(JobPart, pk=jobpartid)
    if not canAccess(request.user, job):
        return HttpResponse(status=401)

    element = request.POST.get("element")
    value = request.POST.get("value")

    # only allow explicit columns to be saved
    if element and value:
        if element == 'status':
            jobpart.status = value

    jobpart.save()

    return render(request, 'blocks/part_row.html', {
        'jobpart': jobpart,
        'part': jobpart.part
    })


'''
Return a list of times for this job
'''


def jobtimes(request, jobid):
    job = get_object_or_404(Job, pk=jobid)
    if not canAccess(request.user, job):
        return HttpResponse(status=401)

    times = JobTime.objects.filter(job_id=jobid)
    return render(request, 'blocks/job_times.html', {
        'timesCollection': times,
        'jobid': jobid
    })


'''
Add an start stamp to the record
'''


def starttime(request, jobid):
    job = get_object_or_404(Job, pk=jobid)
    if not canAccess(request.user, job):
        return HttpResponse(status=401)

    # if they push start, and a job is already running, just return an "ok"
    jobtime = JobTime.objects.filter(end__isnull=True).count()
    if jobtime > 0:
        return HttpResponse(status=200)
    tz = pytz.timezone(settings.TIME_ZONE)
    tech = Technician.objects.get(pk=request.user.id)
    jobtime = JobTime()
    jobtime.job = job
    jobtime.technician = tech
    jobtime.start = datetime.now(tz)
    jobtime.save()
    return HttpResponse(status=200)


'''
Add an end stamp to the record
'''


def stoptime(request, jobid):
    job = get_object_or_404(Job, pk=jobid)
    if not canAccess(request.user, job):
        return HttpResponse(status=401)

    # if they push start, and a job is already running, just return an "ok"
    jobtimeCollection = JobTime.objects.filter(end__isnull=True)[:1]

    if jobtimeCollection.count() == 0:
        return HttpResponse(status=200, content="No job started")

    jobtime = jobtimeCollection[0]

    tz = pytz.timezone(settings.TIME_ZONE)
    jobtime.end = datetime.now(tz)
    jobtime.save()
    return HttpResponse(status=200)


'''
Add an end stamp to the record
'''


def removetime(request, jobid, timeid):
    job = get_object_or_404(Job, pk=jobid)
    time = get_object_or_404(JobTime, pk=timeid)
    if not canAccess(request.user, job):
        return HttpResponse(status=401)

    time.delete()

    return HttpResponse(status=200)


'''
Add comment to a time record
'''


def addtimecomment(request, jobid, timeid):
    job = get_object_or_404(Job, pk=jobid)
    time = get_object_or_404(JobTime, pk=timeid)
    if not canAccess(request.user, job):
        return HttpResponse(status=401)

    text = request.POST.get("text", "")
    time.comment = text
    time.save()
    return HttpResponse(status=200)


'''
Updates various elements of the job
'''


def updatejob(request, jobid):
    job = get_object_or_404(Job, pk=jobid)
    if not canAccess(request.user, job):
        return HttpResponse(status=401)

    element = request.POST.get("element")
    value = request.POST.get("value")

    if element and value:
        if element == 'status':
            job.status = value
        if element == 'level':
            job.level = value
        if element == 'appointment':
            tz = pytz.timezone(settings.TIME_ZONE)
            datetimeappt = parse_datetime(value)
            datetimeappt = datetimeappt.replace(tzinfo=tz)
            job.appointment = datetimeappt
        job.save()

    return render(request, 'blocks/job_row.html', {
        'job': job,
    })
