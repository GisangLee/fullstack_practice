from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):

    help = "This command creates houserules"
    # def add_arguments(self, parser):
    #     parser.add_argument("--times", help="how many times")

    def handle(self, *args, **options):
        houserules = [
            "키패드로 셀프 체크인",
            "열쇠 보관함으로 체크인",
            "안내 직원(으)로 셀프 체크인",
            "흡연 금지",
            "반려동물 동반 불가",
            "어린이와 유아에게 적합하지 않음",
            "파티 또는 이벤트 금지",
        ]

        for r in houserules:
            room_models.HouseRule.objects.create(name=r)

        self.stdout.write(self.style.SUCCESS("Houserules Created"))