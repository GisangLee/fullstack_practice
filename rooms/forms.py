from django import forms
from . import models as room_models
from django_countries.fields import CountryField


class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere", label="도시", required=False)
    country = CountryField(default="KR").formfield()

    price = forms.IntegerField(required=False, label="가격")
    guests = forms.IntegerField(required=False, label="게스트")
    beds = forms.IntegerField(required=False, label="침대")
    bedrooms = forms.IntegerField(required=False, label="침실")
    baths = forms.IntegerField(required=False, label="화장실")

    instant_book = forms.BooleanField(required=False, label="즉석 예약")
    host = forms.BooleanField(required=False, label="호스트")

    room_type = forms.ModelChoiceField(
        required=False,
        empty_label="숙소 전체",
        label="숙소 유형",
        queryset=room_models.RoomType.objects.all()
    )

    amenities = forms.ModelMultipleChoiceField(
        required=False,
        label="편의시설",
        queryset=room_models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        label="숙박시설",
        queryset=room_models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class CreatePhotoForm(forms.ModelForm):

    class Meta:
        model = room_models.Photo
        fields = (
            "caption",
            "file",
        )
        
    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        room = room_models.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()

