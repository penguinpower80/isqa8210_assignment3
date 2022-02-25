'''
Return a date format string
'''
def getDateFormat():
    return "%m/%d/%Y"

'''
Return a time format string
'''
def getTimeFormat():
    return "%-I:%M %p"

'''
Return a date time format string
'''
def getDateTimeFormat():
    return getDateFormat() + " at " + getTimeFormat()