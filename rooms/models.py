from django.db import models
from django.urls import reverse
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
class Facility(AbstractItem):
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

    """   
       related_name 은 외래키의 대상이(예를 들어 여러 숙박시설은 한 명의 호스트를 갖을 때, 그 호스트를 말함) 외래키 정보에 접근할 때 사용
    """
    host = models.ForeignKey(user_models.User, related_name="rooms", on_delete=models.CASCADE)
    roomtype = models.ForeignKey(RoomType, related_name="rooms", on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(Amenity, related_name="rooms", blank=True)
    facilities = models.ManyToManyField(Facility, related_name="rooms", blank=True)
    houserules = models.ManyToManyField(HouseRule, related_name="rooms", blank=True)

    def __str__(self):
        return self.room_name

    # Django의 모든 Model은 save 메서드가 존재한다
    # save 메서드를 오버라이딩하여 진짜 save되기 전에 이벤트를 인터럽트하는 과정
    # 예를 들어 데이터가 저장되기 전, seoul을 Seoul로 변경하기 위해 이벤트를 인터럽트한 후 Seoul을 저장하기 위해 Django Model의 save 메서드를 실행
    # 부모 메서드를 사용하기 위해 super() 사용
    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    # Admin 사이트에서 절대 경로로 해당 모델의 URL로 접근하는 시스템 구축
    # reverse(config.urls:rooms.urls)
    def get_absolute_url(self):
        return reverse("rooms:room_detail", kwargs={'pk': self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_avg()
            return round(all_ratings / len(all_reviews), 2)
        return 0

    def cleanliness_avg(self):
        all_cleanliness = self.reviews.all()
        cleanliness_rating = 0
        if len(all_cleanliness) > 0:
            for single_cleanliness in all_cleanliness:
                cleanliness_rating += single_cleanliness.send_cleanliness()
            return round(cleanliness_rating / len(all_cleanliness), 2)
        return 0
            
    def location_avg(self):
        all_location = self.reviews.all()
        location_rating = 0
        if len(all_location) > 0:
            for single_location in all_location:
                location_rating += single_location.send_location()
            return round(location_rating / len(all_location), 2)
        return 0
            
    def accuray_avg(self):
        all_accuracy = self.reviews.all()
        accuracy_rating = 0
        if len(all_accuracy) > 0:
            for single_accuracy in all_accuracy:
                accuracy_rating += single_accuracy.send_accuracy()
            return round(accuracy_rating / len(all_accuracy), 2)
        return 0
            
    def check_in_avg(self):
        all_check_in = self.reviews.all()
        check_in_rating = 0
        if len(all_check_in) > 0:
            for check_in_accuracy in all_check_in:
                check_in_rating += check_in_accuracy.send_check_in()
            return round(check_in_rating / len(all_check_in), 2)
        return 0
            
    def communication_avg(self):
        all_communication = self.reviews.all()
        communication_rating = 0
        if len(all_communication) > 0:
            for single_communication in all_communication:
                communication_rating += single_communication.send_communication()
            return round(communication_rating / len(all_communication), 2)
        return 0
            
    def pricesatisfaction_avg(self):
        all_pricesatisfaction = self.reviews.all()
        pricesatisfaction_rating = 0
        if len(all_pricesatisfaction) > 0:
            for single_pricesatisfaction in all_pricesatisfaction:
                pricesatisfaction_rating += single_pricesatisfaction.send_pricesatisfaction()
            return round(pricesatisfaction_rating / len(all_pricesatisfaction), 2)
        return 0
            

        
# 룸 사진
class Photo(core_models.TimeStampModel):
    caption = models.CharField(max_length=100)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey(Room, related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption