from django.db import models


class UserTypes(models.TextChoices):
    CUSTOMER = 'C', 'Customer'
    TECHNICIAN = 'T', 'Technician'
    STAFF = 'S', 'Staff'

class JobStatus(models.TextChoices):
    NEW = 'N', 'New'
    OPEN = 'O', 'Open'
    CANCEL = 'X', 'Cancelled'
    HOLD = 'H', 'Hold'
    WAITING = 'W', 'Waiting'
    COMPLETE = 'C', 'Complete'


class PartStatus(models.TextChoices):
    WAREHOUSE = 'W', 'At the warehouse'
    UNAVAILABLE = 'U', 'Not Available'
    DISCONTINUED = 'D', 'Discontinued'
    ORDER = 'O', 'Order'


class JobLevel(models.TextChoices):
    LOW = 'L', 'Low Urgency'
    NORMAL = 'N', 'Normal Urgency'
    CRITICAL = 'C', 'Critical Urgency'


class PartLocation(models.TextChoices):
    PENDING = 'P', 'Pending'
    DISPATCHED = 'D', 'Dispatched'
    TECHNICIAN = 'T', 'With the Technician'
    ORDERED = 'O', 'Ordered'
    INSTALLED = 'I', 'Installed'
    CANCELED = 'C', 'Cancelled'