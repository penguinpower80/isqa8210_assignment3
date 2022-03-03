import logging

from django import template
from django.contrib.humanize.templatetags import humanize
from django.template.loader import render_to_string

from django.utils.safestring import mark_safe

from tech.helpers.helpers import getDateTimeFormat, generateJsonSelections, selectorBuilder
from tech.models import JobLevel, Part, JobStatus, PartLocation

register = template.Library()


@register.simple_tag()
def level_badge(status):
    r = ''
    if status == JobLevel.NORMAL:
        r = '<span class="tag is-warning">Medium</span>'

    if status == JobLevel.LOW:
        r = '<span class="tag is-success">Normal</span>'

    if status == JobLevel.CRITICAL:
        r = '<span class="tag is-danger">High</span>'

    return mark_safe(r)


@register.simple_tag()
def appt(appt, jobid):
    if appt:
        return mark_safe('<div class="tag is-primary is-light is-large iscustomerappt" data-jobid='+ str(jobid) +' data-appt="' +
                         appt.strftime("%Y-%m-%d %H:%M:%S") + '">'
                         '<span class="icon">'
                         '<i class="fas fa-calendar"></i>'
                         '</span>'
                         '<span>'
                         '<span class="is-hidden-mobile">'
                         'Appointment: '
                         '</span>' +
                         appt.strftime(getDateTimeFormat()) +
                         ' <span class="is-hidden-mobile">'
                         '(' + humanize.naturaltime(appt) + ')'
                                                            '</span>'
                                                            '</span>'
                                                            '</div>')
    else:
        return mark_safe('<div class="tag is-primary is-light is-large iscustomerappt" data-jobid='+ str(jobid) +' data-appt="">'
                         '<span class="icon">'
                         '<i class="fas fa-calendar"></i>'
                         '</span>'
                         '<span>'
                         '<span class="is-hidden-mobile">'
                         'Appointment: '
                         '</span>NO APPOINTMENT SET<span class="is-hidden-mobile">'                         
                                                            '</span>'
                                                            '</span>'
                                                            '</div>')


@register.simple_tag()
def jobage(created):
    return humanize.naturalday(created)


@register.simple_tag()
def partslist(jobid):
    partCollection = Part.objects.all()
    s = '<div class="add_part_holder">'
    for part in partCollection:
        s += render_to_string('blocks/single_part.html', {'part': part, 'jobid': jobid})
    s += "</div>"
    return mark_safe(s)


@register.simple_tag()
def timeworked(start, end):
    if not end:
        return ''
    diff = end - start
    days = diff.days
    hours, leftover = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(leftover, 60)
    time_string = []
    if days > 0:
        time_string.append(str(days) + ' day(s)')
    if hours > 0:
        time_string.append(str(hours) + ' hour(s)')
    if minutes > 0:
        time_string.append(str(minutes) + ' minute(s)')
    return ",".join(time_string)


@register.simple_tag
def status_picker(status, jobid=None, classsuffix='selector', alloption=False, alltext='All Status'):
    s = selectorBuilder(JobStatus.choices, status, jobid, 'status', 'jobstatus' + classsuffix, alloption, alltext)
    return mark_safe(s)


@register.simple_tag
def level_picker(level, jobid=None, classsuffix='selector', alloption=False, alltext='All Levels'):
    s = selectorBuilder(JobLevel.choices, level, jobid, 'level', 'joblevel'+classsuffix, alloption, alltext)
    return mark_safe(s)


@register.simple_tag
def joblevels():
    return mark_safe(generateJsonSelections(JobLevel.choices))


@register.simple_tag
def jobstatii():
    return mark_safe(generateJsonSelections(JobStatus.choices))


@register.simple_tag
def partstatii():
    return mark_safe(generateJsonSelections(PartLocation.choices))


@register.simple_tag(takes_context=True)
def jobtimebutton(context, job):
    if not context.request.user.is_tech():
        return ''
    active = job.jobtime_set.filter(end__isnull=True).count()
    return mark_safe('<button class ="button is-' + (
        "danger" if active == 1 else "success") + ' is-fullwidth togglejobtimer" data-active="' + str(
        active) + '" data-job="' + str(job.id) + '" >'
                                                 '<span class="icon">'
                                                 '<i class="fas fa-' + ("stop" if active == 1 else "play") + '"></i>'
                                                                                                             '</span>'
                                                                                                             '<span class="timertext"> ' + (
                         "Stop" if active == 1 else "Start") + ' Time </span>'
                                                               '</button>')
