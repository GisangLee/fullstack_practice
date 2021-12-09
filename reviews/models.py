from django.db import models
from core import models as core_models
from users import models as user_models
from rooms import models as room_models


class Review(core_models.TimeStampModel):
    """ 후기 Definition """
    description = models.TextField()
    cleanliness = models.DecimalField(decimal_places=1, max_digits=2)
    location = models.DecimalField(decimal_places=1, max_digits=2)
    accuracy = models.DecimalField(decimal_places=1, max_digits=2)
    check_in = models.DecimalField(decimal_places=1, max_digits=2)
    communication = models.DecimalField(decimal_places=1, max_digits=2)
    pricesatisfaction = models.DecimalField(decimal_places=1, max_digits=2)
    user = models.ForeignKey(user_models.User, related_name="reviews", on_delete=models.CASCADE)
    room = models.ForeignKey(room_models.Room, related_name="reviews", on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    def rating_avg(self):
        avg = (
            self.cleanliness +
            self.location +
            self.accuracy +
            self.check_in +
            self.communication +
            self.pricesatisfaction
        ) / 6
        return round(avg, 2)
    
    def send_cleanliness(self):
        return self.cleanliness

    def send_location(self):
        return self.location
    
    def send_accuracy(self):
        return self.accuracy

    def send_check_in(self):
        return self.check_in

    def send_communication(self):
        return self.communication

    def send_pricesatisfaction(self):
        return self.pricesatisfaction
    
    # Admin 열제목 바꾸기
    rating_avg.short_description = "Rating Average"
    
