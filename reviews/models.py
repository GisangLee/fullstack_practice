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
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    room = models.ForeignKey(room_models.Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.description
