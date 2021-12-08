from django.contrib import admin
from . import models


@admin.register(models.Review)
class RegisterAdmin(admin.ModelAdmin):

    """ 후기 Admin Definition """
    list_display = admin.ModelAdmin.list_display + ("user", "room",)