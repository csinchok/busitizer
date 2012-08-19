from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from busitizer.core.models import Photo


class Command(BaseCommand):
    args = ''
    help = 'Clears out all the photos. Helps with testing.'

    def handle(self, *args, **options):
    	for photo in Photo.objects.all():
            photo.delete()