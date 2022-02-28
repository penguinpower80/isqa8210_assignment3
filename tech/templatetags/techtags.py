import datetime
import logging

from django import template
from django.contrib.humanize.templatetags import humanize
from django.template.loader import render_to_string

from django.utils.safestring import mark_safe

from tech.helpers.helpers import getDateTimeFormat, timeWorked
from tech.models import JobLevel, Part, JobStatus

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
def appt(appt):
    return mark_safe('<div class="tag is-primary is-light is-large">'
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
    diff = end-start
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
def status_picker(status, jobid):
    s='<select class="select" id="jobstatus_' + str(jobid) +'">'
    for choice in JobStatus.choices:
        selected = 'selected="SELECTED"' if status==choice[0] else ''
        s+="<option {} value='{}'>{}</option>".format(selected, choice[0], choice[1])
    s+='</select>'
    return mark_safe(s)

@register.simple_tag
def level_picker(level, jobid):
    s='<select class="select" id="joblevel_' + str(jobid) +'">'
    for choice in JobLevel.choices:
        selected = 'selected="SELECTED"' if level==choice[0] else ''
        s+="<option {} value='{}'>{}</option>".format(selected, choice[0], choice[1])
    s+='</select>'
    return mark_safe(s)