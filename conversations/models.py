from django.db import models
from core import models as core_models
from users import models as user_models


class Conversation(core_models.TimeStampModel):
    """ 대화 Definition """
    participants = models.ManyToManyField(user_models.User, blank=True)

    def __str__(self):
        return str(self.created_at)


class Message(core_models.TimeStampModel):
    """ 메세지 Definition """
    message = models.TextField()
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    place = models.ForeignKey(Conversation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} says: {self.message}"