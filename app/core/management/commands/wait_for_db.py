import time 
from django.db import connections
from django.db.utils import  OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """  Django custom command to pause project startup
    until the database connection is available and ready 
    to accept connections 
    """
    def handle(self, *args, **options):
        self.stdout.write("waiting for database connection ....")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except  OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1) ## wait 1 sec then try again
        # after successfully connected 
        self.stdout.write(self.style.SUCCESS('Database available!'))
