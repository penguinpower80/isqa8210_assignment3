import datetime


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


def timeWorked( seconds ):
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
