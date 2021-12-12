from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User


class Command(BaseCommand):

    help = "This command creates users"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=2, type=int, help="how many users do you want")

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(User, number, {
            "is_staff": False,
            "is_superuser": False,
            "language": "kr",
            "eamil_verified": False,
            "email_secret": "",
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} of users Created"))