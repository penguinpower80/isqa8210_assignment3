import logging

import weasyprint
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

from tech.helpers.helpers import canAccess
from tech.models import Job, JobPart


def html(request, jobid):
    job = get_object_or_404(Job, pk=jobid)
    if not canAccess(request.user, job):
        return HttpResponse(status=401)

    return render(request, 'tech/invoice.html', { 'job':job, 'isHtml': True })

def pdf(request, jobid):

    job = get_object_or_404(Job, pk=jobid)
    if not canAccess(request.user, job):
        return HttpResponse(status=401)
    html = render_to_string('tech/invoice.html', {'job':job})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=job_{job.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '\\css\\pdf.css')])
    return response
