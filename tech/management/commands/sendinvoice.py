from django.conf import settings
from django.core.management import BaseCommand

# https://docs.djangoproject.com/en/4.0/topics/email/
from tech.helpers.helpers import send_invoice
from tech.models import Job

'''
This command allows a specific invoice to be sent from the command line.
usage: pythan manage.py sendinvoice (invoice number/job id) [recipient email]
Valid invoice number must be provided!
'''
class Command(BaseCommand):
    help = "Send Invoice."

    def add_arguments(self, parser):
        parser.add_argument('job', help="Job to send invoice for.")
        parser.add_argument('to', nargs='?', help="Email to send it to.")

    def handle(self, *args, **options):
        if not options['job']:
            self.stdout.write('No job specified.')
            return

        job_id = int(options['job'])
        try:
            thisjob = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            self.stdout.write('Job not found.')
            return

        send_invoice(thisjob, options['to'])

        if settings.EMAIL == 'LOCAL':
            self.stdout.write('Check "/{}" for emails'.format(settings.EMAIL_FILE_PATH))
