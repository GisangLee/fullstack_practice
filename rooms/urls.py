from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>/", views.RoomDetail.as_view(), name="room_detail"),
    path("<int:pk>/update_room/", views.UpdateRoomView.as_view(), name="update_room"),
    path("<int:pk>/photos/", views.UpdateRoomPhotos.as_view(), name="update_photos"),
    path("search/", views.SearchView.as_view(), name="search"),
]