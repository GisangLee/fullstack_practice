import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews import models as review_models
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):

    help = "This command creates reviews"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=2, type=int, help="how many reviews do you want")

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()

        seeder.add_entity(review_models.Review, number, {
            "cleanliness": lambda x: float(random.randrange(155, 389))/100,
            "location": lambda x: float(random.randrange(155, 389))/100,
            "accuracy": lambda x: float(random.randrange(155, 389))/100,
            "check_in": lambda x: float(random.randrange(155, 389))/100,
            "communication": lambda x: float(random.randrange(155, 389))/100,
            "pricesatisfaction": lambda x: float(random.randrange(155, 389))/100,
            "user": lambda x: random.choice(all_users),
            "room": lambda x: random.choice(all_rooms),
        })

        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} of reviews Created"))