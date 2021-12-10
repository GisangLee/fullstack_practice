# from math import ceil
# from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django_countries import countries
# from django.core.paginator import EmptyPage, Paginator
from rooms import models as room_models
from . import forms

""" DJango의 Class Bases View인 list View를 활용한 페지네이션"""


class HomeView(ListView):
    model = room_models.Room
    ordering = "created_at"
    paginate_by = 10
    paginate_orphans = 5
    context_object_name = "rooms"


""" CBV방식의 숙박 보여주기 방식"""


class RoomDetail(DetailView):
    model = room_models.Room


""" FBV 방식의 숙박 보여구기 방식


def room_detail(request, pk):
    try:
        room = room_models.Room.objects.get(pk=pk)
        return render(
            request,
            "rooms/room_detail.html",
            context={"room": room}
        )
    except room_models.Room.DoesNotExist:
        raise Http404()
"""


""" Django Form API를 사용한 숙소 검색 """


def search_rooms(request):

    form = forms.SearchForm()

    return render(
        request,
        "rooms/room_search.html",
        context={
            "form": form,
        }
    )


""" Django Form API를 사용하지 않고 수동으로 작성하는 숙소 검색


def search_rooms(request):
    city = request.GET.get("city", "anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", "4"))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    beds = int(request.GET.get("beds", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    baths = int(request.GET.get("baths", 0))

    instant = bool(request.GET.get("instant", False))
    super_host = bool(request.GET.get("super_host", False))

    roomt_types = room_models.RoomType.objects.all()
    amenities = room_models.Amenity.objects.all()
    facilities = room_models.Facility.objects.all()

    selected_amenities = request.GET.getlist("amenities")
    selected_facilities = request.GET.getlist("facilities")

# request로 받는 것들(form)과 DB에서 가져오는 것들(choices)을 분리하여 Dict형태로 구분
    form = {
        "city": city,
        "selected_country": country,
        "selected_room_type": room_type,
        "price": price,
        "guests": guests,
        "beds": beds,
        "bedrooms": bedrooms,
        "baths": baths,
        "selected_amenities": selected_amenities,
        "selected_facilities": selected_facilities,
        "instant": instant,
        "super_host": super_host,
    }

    choices = {
        "countries": countries,
        "room_types": roomt_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city
    
    filter_args["country"] = country

    if room_type != 4:
        filter_args["roomtype__pk"] = room_type

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__lte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__lte"] = bedrooms

    if baths != 0:
        filter_args["baths__lte"] = baths

    if beds != 0:
        filter_args["beds__lte"] = beds

    if instant is True:
        filter_args["instant_book"] = True
    
    if super_host is True:
        filter_args["host__superhost"] = True

    rooms = room_models.Room.objects.filter(**filter_args)

    if len(selected_amenities) > 0:
        for amenity_id in selected_amenities:
            rooms = rooms.filter(amenities__pk=int(amenity_id))

    if len(selected_facilities) > 0:
        for facility_id in selected_facilities:
            rooms = rooms.filter(facilities__pk=int(facility_id))

    print(filter_args)
    print(rooms)

    return render(
        request,
        "rooms/room_search.html",
        context={
            **form,
            **choices,
        }
    )
"""


# def show_all_rooms(request):
""" DJango 의 Paginator를 이용한 페지네이션

    page = request.GET.get("page", 1)
    room_list = room_models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)

    try:
        rooms = paginator.page(int(page))
        return render(
            request,
            "rooms/home.html",
            context={
                "rooms": rooms,
            }
        )
    except EmptyPage:
        return redirect("/")
"""

""" 오직 Python을 활용한 페지네이션
    
    page = request.GET.get("page", 1)
    page = int(page or 1)
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    page_conut = ceil(room_models.Room.objects.count() / page_size)

    all_rooms = room_models.Room.objects.all()[offset:limit]
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
            "page": page,
            "page_count": page_conut,
            "page_range": range(1, page_conut)
        }
    )
"""
