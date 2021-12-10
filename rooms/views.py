# from math import ceil
from django.views.generic import ListView
from django.utils import timezone
# from django.shortcuts import render, redirect
# from django.core.paginator import EmptyPage, Paginator
from rooms import models as room_models


""" DJango의 Class Bases View인 list View를 활용한 페지네이션"""


class HomeView(ListView):
    model = room_models.Room
    ordering = "created_at"
    paginate_by = 10
    paginate_orphans = 5
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

#def show_all_rooms(request):
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
