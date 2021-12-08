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
    host = models.ForeignKey(user_models.User, related_name="rooms", on_delete=models.CASCADE)

    roomtype = models.ForeignKey(RoomType, related_name="rooms", on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(Amenity, related_name="rooms", blank=True)
    facilities = models.ManyToManyField(Facilitiy, related_name="rooms", blank=True)
    houserules = models.ManyToManyField(HouseRule, related_name="rooms", blank=True)

    def __str__(self):
        return self.room_name

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.rating_avg()
        return all_ratings / len(all_reviews)

    def cleanliness_avg(self):
        all_cleanliness = self.reviews.all()
        cleanliness_rating = 0
        for single_cleanliness in all_cleanliness:
            cleanliness_rating += single_cleanliness.send_cleanliness()
        return cleanliness_rating / len(all_cleanliness)

    def location_avg(self):
        all_location = self.reviews.all()
        location_rating = 0
        for single_location in all_location:
            location_rating += single_location.send_location()
        return location_rating / len(all_location)

    def accuray_avg(self):
        all_accuracy = self.reviews.all()
        accuracy_rating = 0
        for single_accuracy in all_accuracy:
            accuracy_rating += single_accuracy.send_accuracy()
        return accuracy_rating / len(all_accuracy)

    def check_in_avg(self):
        all_check_in = self.reviews.all()
        check_in_rating = 0
        for check_in_accuracy in all_check_in:
            check_in_rating += check_in_accuracy.send_check_in()
        return check_in_rating / len(all_check_in)

    def communication_avg(self):
        all_communication = self.reviews.all()
        communication_rating = 0
        for single_communication in all_communication:
            communication_rating += single_communication.send_communication()
        return communication_rating / len(all_communication)
    
    def pricesatisfaction_avg(self):
        all_pricesatisfaction = self.reviews.all()
        pricesatisfaction_rating = 0
        for single_pricesatisfaction in all_pricesatisfaction:
            pricesatisfaction_rating += single_pricesatisfaction.send_pricesatisfaction()
        return pricesatisfaction_rating / len(all_pricesatisfaction)

        
# 룸 사진
class Photo(core_models.TimeStampModel):
    caption = models.CharField(max_length=100)
    file = models.ImageField()
    room = models.ForeignKey(Room, related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption