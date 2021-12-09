from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):

    help = "This command creates facilities"
    # def add_arguments(self, parser):
    #     parser.add_argument("--times", help="how many times")

    def handle(self, *args, **options):
        facilities = [
            "게스트 전용 출입구",
            "엘리베이터",
            "주차 공간",
            "헬스장",
            "유료 내부 주차장",
            "유료 외부 주차장",
        ]

        for f in facilities:
            room_models.Facility.objects.create(name=f)

        self.stdout.write(self.style.SUCCESS("Facilities Created"))