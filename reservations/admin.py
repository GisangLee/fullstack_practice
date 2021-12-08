from django.contrib import admin
from . import models


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """ 예약 Admin Definition """

    list_display = (
        "room",
        "guest",
        "check_in",
        "check_out",
        "status",
        "is_progress",
        "is_finished",
    )

    list_filter = ("status",)