from django.db import models
from core import models as core_models
from users import models as user_models


class Conversation(core_models.TimeStampModel):
    """ 대화 Definition """
    participants = models.ManyToManyField(user_models.User, related_name="conversations", blank=True)

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)
        return ", ".join(usernames)

    def count_messages(self):
        return self.messages.count()
    
    def count_participants(self):
        return self.participants.count()

    count_messages.short_description = "Number of Messages"
    count_participants.short_description = "Number of participants"


class Message(core_models.TimeStampModel):
    """ 메세지 Definition """
    message = models.TextField()
    user = models.ForeignKey(user_models.User, related_name="messages", on_delete=models.CASCADE)
    place = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} says: {self.message}"