from django.contrib import admin
from . import models


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = admin.ModelAdmin.list_display + ("count_messages", "count_participants",)


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = admin.ModelAdmin.list_display + ("created_at",)

