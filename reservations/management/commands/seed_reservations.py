import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations import models as reservation_models
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):

    help = "This command creates reservations"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=2, type=int, help="how many reservations do you want")

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()

        seeder.add_entity(reservation_models.Reservation, number, {
            "status": lambda x: random.choice(["pending", "confirmed", "cancled"]),
            "guest": lambda x: random.choice(all_users),
            "room": lambda x: random.choice(all_rooms),
            "check_in": lambda x: datetime.now(),
            "check_out": lambda x: datetime.now() + timedelta(days=random.randint(3, 25))
        })

        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} of reservations Created"))