from django.contrib import admin
from . import models


@admin.register(models.RoomType, models.Amenity, models.Facilitiy, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """ 건물 형태, 편의 시설, 숙박 예의, 숙박 규칙 Definition """
    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ 숙박 Admin Definition """
    list_display = admin.ModelAdmin.list_display + ("address", "check_in", "check_out", "host",)


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ 숙박 사진 Admin Definition """
    pass