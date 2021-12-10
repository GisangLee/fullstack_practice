import random
from django.contrib.admin.utils import flatten
from django.core.management.base import BaseCommand
from django_seed import Seed
from users import models as user_models
from rooms import models as room_models
from lists import models as list_models


class Command(BaseCommand):

    help = "This command creates lists"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=2, type=int, help="how many lists do you want")

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()

        seeder.add_entity(list_models.List, number, {
            "user": lambda x: random.choice(all_users),
        })

        created_lists = seeder.execute()
        created_clean = flatten(list(created_lists.values()))

        for pk in created_clean:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = all_rooms[random.randint(0, 5):random.randint(6, 30)]
            list_model.room.add(*to_add)
        self.stdout.write(self.style.SUCCESS(f"{number} of lists Created"))