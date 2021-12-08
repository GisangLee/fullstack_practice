from django.contrib import admin
from . import models


@admin.register(models.RoomType, models.Amenity, models.Facilitiy, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """ 건물 형태, 편의 시설, 숙박 예의, 숙박 규칙 Definition """

    list_display = (
        "name",
        "used_by",
    )
    
    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ 숙박 Admin Definition """
    list_display = admin.ModelAdmin.list_display + (
        "address",
        "check_in",
        "check_out",
        "host",
        "room_name",
        "country",
        "city",
        "price",
        "beds",
        "bedrooms",
        "baths",
        "guests",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    ordering = ("room_name", "price",)

    list_filter = (
        "instant_book",
        "city",
        "roomtype",
        "amenities",
        "facilities",
        "houserules",
        "country",
    )

    search_fields = ("=city", "^host__username",)

    filter_horizontal = ("amenities", "facilities", "houserules",)

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("room_name", "description", "country", "address", "price",)}
        ),

        (
            "Times",
            {"fields": ("check_in", "check_out", "instant_book",)}
        ),

        (
            "Spaces",
            {"fields": ("beds", "bedrooms", "baths", "guests",)}
        ),

        (
            "More About Space",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "houserules",)
            }
        ),

        (
            "Last Details",
            {"fields": ("host",)}
        )
    )

    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ 숙박 사진 Admin Definition """
    pass