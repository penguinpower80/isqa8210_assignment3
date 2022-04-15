import datetime
import logging
from django.conf import settings

import weasyprint
from decouple import config

from django.core.mail import send_mail, EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse

from tech.models import *


def getDateFormat():
    """
    Return a date format string
    :return:string
    """
    return "%m/%d/%Y"


def getTimeFormat():
    """
    Return a time format string
    :return:string
    """
    return "%#I:%M %p"


def getDateTimeFormat():
    """
    Return a date time format string
    :return: string
    """
    return getDateFormat() + " at " + getTimeFormat()


def timeWorked(seconds: int):
    """
    Generate a time worked string
    :param int seconds: total seconds
    :return: string
    """
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


def canAccess(user, job):
    """
    Checks if the current user is authenticated AND has a connection to the job in quest

    :param User user: A User object
    :param Job job: A Job object
    :return: boolean
    """
    if not user.is_authenticated:
        return False

    return job.technician_id == user.id or job.customer_id == user.id or user.is_superuser


def generateJsonSelections(choices):
    """
    Generate a JS object for use in pop-ups
    :param models.TextChoices choices:
    :return: string
    """
    options = []
    for option in choices:
        options.append(option[0] + ':' + "'{}'".format(option[1]))
    return '{' + ",".join(options) + '}'


def roundFifteen(minutes: int) -> float:
    """
    Round minutes to nearest quarter hour for billing.
    :param integer minutes:
    :return: float
    """
    hours, leftover = divmod(minutes, 60)
    fullquarters = leftover // 15

    remainder = leftover % 15
    if remainder > 7.5:  # did they work more than 7 1/2 minutes, so charge for the 15 minute block
        fullquarters += 1
    hours = hours + (fullquarters / 4)
    return hours


def selectorBuilder(choices, selected_value, jobid=None, name='', class_name='ttselector', all_option=False,
                    all_text='All'):
    """
    Build the HTML select and options.  Used in template tags.
    :param models.TextChoices choices:
    :param string selected_value:
    :param int jobid:
    :param string name:
    :param string class_name:
    :param boolean all_option:
    :param string all_text:
    :return: string
    """
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
    """
    Build a URL with a msg parameter added to it
    :param int|string message: The id of a message to include
    :param string location: The target url
    :return: redirect
    """
    base_url = reverse(location)
    url = '{}?msg={}'.format(base_url, message)
    return redirect(url)


def getMessageText(mIdx):
    """
    Given a specific index number, returns a message.
    Security precaution to not let arbitrary messages be passed.  Maybe an (unlikely??) attack vector?
    :param integer mIdx:
    :return: string
    """
    if mIdx == 1:
        return 'Thank you for submitting your request.  We will review it and get back to you shortly.'
    if mIdx == 2:
        return 'Profile Saved.'


def send_invoice(job, to=None):
    """
    Sends an invoice for a specific job.  Optionally allows the recipient to be overwritten (for testing)
    Note to self: this would be better done if the email were queued for generation and sending, not done synchronously like here -> possible performance
    issues!!
    Template from: https://www.hiveage.com/blog/how-to-write-invoice-email/
    :param Job job:
    :param string to:
    """
    completed_string = job.updated_at.strftime(getDateTimeFormat())

    due = job.updated_at + datetime.timedelta(days=30)
    due_string = due.strftime(getDateFormat())

    subject = f"TechTracker Invoice #{job.id}, due {due_string}"
    template_file = open('tech/assets/emails/invoice.tpl', "r")
    message = template_file.read().replace("{{client}}", job.customer.name()).replace("{{number}}", str(job.id)).replace("{{due}}", due_string).replace('{{issue}}', job.description).replace(
        '{{completed}}', completed_string)

    if to is not None:
        recipients = [to]
    elif config('FORCED_INVOICE_EMAIL', default=None) is not None:
        recipients = [config('FORCED_INVOICE_EMAIL')]
    else:
        recipients = [job.customer.email]

    email = EmailMessage(
        subject,
        message,
        config('FROM'),
        recipients
    )

    pdf_content = render_to_string('tech/invoice.html', {'job': job})

    pdf = weasyprint.HTML(string=pdf_content).write_pdf(stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')])

    email.attach(f'invoice_{job.id}.pdf', pdf, 'application/pdf')
    email.send(fail_silently=False)
