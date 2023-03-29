from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Deletes current and recreates the mock database'

    def handle(self, *args, **options):
        """ Call the command """

        # Verify migrations are made and db gets them
        call_command("makemigrations")
        call_command("migrate")

        # Start creating mock data and relations
        print("Mocking up the database...")
