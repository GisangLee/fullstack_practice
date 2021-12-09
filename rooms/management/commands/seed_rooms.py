import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "This command creates rooms"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=2, type=int, help="how many rooms do you want")

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_user = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        houserules = room_models.HouseRule.objects.all()

        seeder.add_entity(room_models.Room, number, {
            "room_name": seeder.faker.address(),
            "host": lambda x: random.choice(all_user),
            "roomtype": lambda x: random.choice(room_types),
            "price": lambda x: random.randint(1, 300),
            "beds": lambda x: random.randint(1, 5),
            "bedrooms": lambda x: random.randint(1, 5),
            "baths": lambda x: random.randint(1, 5),
            "guests": lambda x: random.randint(1, 20),
        })

        created_room = seeder.execute()
        created_clean = flatten(list(created_room.values()))

        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            for _ in range(3, random.randint(10, 30)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 31)}.webp"
                )
            for a in amenities:
                random_number = random.randint(0, 15)
                if random_number % 2 == 0:
                    room.amenities.add(a)
                else:
                    pass

            for f in facilities:
                random_number = random.randint(0, 15)
                if random_number % 2 == 0:
                    room.facilities.add(f)
                else:
                    pass

            for r in houserules:
                random_number = random.randint(0, 15)
                if random_number % 2 == 0:
                    room.houserules.add(r)
                else:
                    pass
            
        self.stdout.write(self.style.SUCCESS(f"{number} of rooms Created"))