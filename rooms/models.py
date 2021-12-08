from django.db import models
from django_countries.fields import CountryField
from core import models as core_models
from users import models as user_models


class AbstractItem(core_models.TimeStampModel):
    """ 건물 유형, 편의시설 등에 사용될 추상 클래스 """

    name = models.CharField(max_length=80)
    
    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# 건물 유형
class RoomType(AbstractItem):
    class Meta:
        verbose_name_plural = "Room types"
        ordering = ["created_at"]


# 숙박 예의
class Amenity(AbstractItem):
    
    class Meta:
        verbose_name_plural = "Amenities"


# 편의 시설
class Facilitiy(AbstractItem):
    class Meta:
        verbose_name_plural = "Facilities"


# 숙박 규칙
class HouseRule(AbstractItem):
    class Meta:
        verbose_name = "House Rule"


class Room(core_models.TimeStampModel):

    """ 숙박 모델 Definition"""
    room_name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    guests = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)

    # 방 주인 (User 모델과 연결)
    host = models.ForeignKey(user_models.User, on_delete=models.CASCADE)

    roomtype = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(Amenity, blank=True)
    facilities = models.ManyToManyField(Facilitiy, blank=True)
    houserules = models.ManyToManyField(HouseRule, blank=True)

    def __str__(self):
        return self.room_name

        
# 룸 사진
class Photo(core_models.TimeStampModel):
    caption = models.CharField(max_length=100)
    file = models.ImageField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.caption