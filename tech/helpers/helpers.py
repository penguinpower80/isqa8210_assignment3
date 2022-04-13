import datetime
import logging

from django.shortcuts import redirect
from django.urls import reverse

'''
Return a date format string
'''


def getDateFormat():
    return "%m/%d/%Y"


'''
Return a time format string
'''


def getTimeFormat():
    return "%#I:%M %p"


'''
Return a date time format string
'''


def getDateTimeFormat():
    return getDateFormat() + " at " + getTimeFormat()


'''
Generate a time worked string
'''


def timeWorked(seconds):
    total_seconds = datetime.timedelta(seconds=seconds)
    days = total_seconds.days
    if total_seconds.seconds > 900:
        hours, leftover = divmod(total_seconds.seconds, 3600)
        minutes, seconds = divmod(leftover, 60)
        time_string = []
        if days > 0:
            time_string.append(str(days) + ' day(s)')
        if hours > 0:
            time_string.append(str(hours) + ' hour(s)')
        if minutes > 0:
            time_string.append(str(minutes) + ' minute(s)')

        return ", ".join(time_string)
    else:
        return "No Time"


'''
Checks if the current user is authenticated AND has a connection to the job in quest
'''


def canAccess(user, job):
    if not user.is_authenticated:
        return False

    return job.technician_id == user.id or job.customer_id == user.id or user.is_superuser


'''
Generate a JS object for use in pop-ups
'''


def generateJsonSelections(choices):
    options = []
    for option in choices:
        options.append(option[0] + ':' + "'{}'".format(option[1]))
    return '{' + ",".join(options) + '}'


def roundFifteen(minutes):
    hours, leftover = divmod(minutes, 60)
    fullquarters = leftover // 15

    remainder = leftover % 15
    if remainder > 7.5: #did they work more than 7 1/2 minutes, so charge for the 15 minute block
        fullquarters += 1
    hours = hours + (fullquarters / 4 )
    return hours


def selectorBuilder(choices, selected_value, jobid=None, name='', class_name='ttselector', all_option=False,
                    all_text='All'):
    s = '<select name="' + name + '" class="select ' + class_name + '" ' + (
        'data-id="' + str(jobid) + '"' if jobid else '') + '>'
    if all_option:
        s += "<option value=''>{}</option>".format(all_text)
    for choice in choices:
        selected = 'selected="SELECTED"' if selected_value == choice[0] else ''
        s += "<option {} value='{}'>{}</option>".format(selected, choice[0], choice[1])
    s += '</select>'
    return s


def getRedirectWithParam(message, location='tech:home'):
    base_url = reverse(location)
    url = '{}?msg={}'.format(base_url, message)
    return redirect(url)

def getMessageText(mIdx):
    if mIdx == 1:
        return 'Thank you for submitting your request.  We will review it and get back to you shortly.'
    if mIdx == 2:
        return 'Profile Saved.'
