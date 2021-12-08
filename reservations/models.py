from django.db import models
from core import models as core_models
from users import models as user_models
from rooms import models as room_models


class Reservation(core_models.TimeStampModel):
    """ 예약 Definition """
    
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "cancled"

    STATUS_CHOICES = (
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_PENDING, "Pending"),
        (STATUS_CANCELED, "Canceled")
    )

    status = models.CharField(choices=STATUS_CHOICES, max_length=12, default=STATUS_PENDING)
    guest = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    room = models.ForeignKey(room_models.Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"{self.room} - f{self.check_in}"