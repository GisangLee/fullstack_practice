from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from rooms import models as room_models

# Register your models here.


class UserInline(admin.TabularInline):
    model = room_models.Room


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin
    list_display = ("username", "email", "gender", "language", "currency", "superhost")
    list_filter = ("superhost", "language", "currency",)
    """

    # 장고에서 지원하는 UserAdmin을 확장시켜 커스텀화 하는 과정

    inlines = (UserInline,)

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "eamil_verified",
        "email_secret",
    )

    fieldsets = UserAdmin.fieldsets + (
        ("Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost"
                )
            }
        ),
    )


""" Custom Model Admin을 만드는 또 하나의 방법. 데코레이터를 사용하는 방법과 아래와 같은 방법이 있다.
admin.site.register(models.User, CustoemUserAdmin)
"""