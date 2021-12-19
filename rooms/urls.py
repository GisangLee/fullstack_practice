from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>/", views.RoomDetail.as_view(), name="room_detail"),
    path("<int:pk>/update_room/", views.UpdateRoomView.as_view(), name="update_room"),
    path("<int:pk>/photos/", views.UpdateRoomPhotos.as_view(), name="update_photos"),
    path("<int:pk>/photos/add/", views.AddPhotoView.as_view(), name="add_photo"),
    path("<int:room_pk>/photos/<int:photo_pk>/delete/", views.delete_photo, name="delete_photo"),
    path("<int:room_pk>/photos/<int:photo_pk>/edit/", views.EditPhotoView.as_view(), name="edit_photo"),
    path("search/", views.SearchView.as_view(), name="search"),
]