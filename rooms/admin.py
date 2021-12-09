from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """ 건물 형태, 편의 시설, 숙박 예의, 숙박 규칙 Definition """

    list_display = (
        "name",
        "used_by",
    )
    
    def used_by(self, obj):
        return obj.rooms.count()


# Inline Admin을 위한 클래스
# TabularInline 또는 StackedInline이 있다. 둘의 차이점은 보이는 게 다르다.
# Room Admin안에 Phtoo Admin을 넣기 위한 작업
class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ 숙박 Admin Definition """

    inlines = (PhotoInline,)

    list_display = admin.ModelAdmin.list_display + (
        "address",
        "check_in",
        "check_out",
        "host",
        "room_name",
        "roomtype",
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

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("room_name", "description", "roomtype", "country", "address", "city", "price",)}
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

    # 많은 리스트가 있을 경우 raw_id_fields를 사용하는 것이 낫다.
    raw_id_fields = ("host",)

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

    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo count"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ 숙박 사진 Admin Definition """
    list_display = admin.ModelAdmin.list_display + ("get_thumbnail",)

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px"src="{obj.file.url}" />')
    
    get_thumbnail.short_description = "room_thumbnail"