import datetime
import logging

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
    return job.technician_id == user.id | job.customer_id == user.id | user.is_superuser


'''
Generate a JS object for use in pop-ups
'''
def generateJsonSelections(choices):
    options = []
    for option in choices:
        options.append(option[0] + ':' + "'{}'".format(option[1]))
    return '{' + ",".join(options) + '}'

def roundFifteen( minutes ):
    fullquarters = minutes // 15
    remainder = minutes % 15
    if remainder > 7.5:
        fullquarters += 15
    if fullquarters == 0:
        return 15

    return fullquarters