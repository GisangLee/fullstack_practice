from django.db import models

# Create your models here.


class TimeStampModel(models.Model):

    """ Time Stamp Model """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 위 모델을 DataBase로 보내지 않기 위한 방법
    class Meta:
        abstract = True
