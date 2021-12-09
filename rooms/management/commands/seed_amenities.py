from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):

    help = "This command creates amenities"
    # def add_arguments(self, parser):
    #     parser.add_argument("--times", help="how many times")

    def handle(self, *args, **options):
        amenities = [
            "식기류",
            "온수",
            "샤워용품",
            "무선 인터넷",
            "난방",
            "업무 전용 공간",
            "주방",
            "냉장고",
            "인덕션",
            "전자레인지",
            "전기밥솥",
            "드리이기",
            "식탁",
            "토스터기",
            "TV",
            "의류 건조대",
            "흡연실",
            "침구",
            "암막커튼",
            "모기장",
            "의류 보관 공간",
            "옷걸이",
            "세탁기 무료 사용",
            "에어컨",
            "화재경보기",
            "소화기",
            "여분의 베개와 담요",
            "바베큐 도구",
            "와인잔",
        ]

        for a in amenities:
            room_models.Amenity.objects.create(name=a)

        self.stdout.write(self.style.SUCCESS("Amenities Created"))