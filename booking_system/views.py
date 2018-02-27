from django.shortcuts import render, redirect
from django.http import HttpResponse
from booking_system.models import Room, Reservation

import datetime



def new_room(request):
    if request.method == 'GET':
        msg_add = "Add new Room"
        return render(request, 'add_edit_room.html', {"msg_add": msg_add})
    elif request.method == 'POST':
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        if request.POST['projector']:
            Room.objects.create(name=name, capacity=capacity, projector=True)
        else:
            Room.objects.create(name=name, capacity=capacity)
        return redirect('/main')



def modify_room(request, id):
    if request.method == 'GET':
        room = Room.objects.get(id=int(id))
        msg_edit = "Edit Room's Data"
        return render(request, 'add_edit_room.html', {"msg_edit": msg_edit, "room": room})
    elif request.method == 'POST':
        room = Room.objects.get(id=int(id))
        for field in ["name", "capacity"]:
            if field in request.POST:
                setattr(room, field, request.POST[field])
        if 'projector' in request.POST:
            room.projector=True
        room.save()
        return redirect('/main')

def delete_room(request, id):
    room = Room.objects.get(id=id)
    room.delete()
    return redirect('/main')

def show_room(request, id):
    room = Room.objects.get(id=id)
    today = datetime.date.today()
    reservations = Reservation.objects.filter(room_booked=room.id, date__gte=today)
    return render(request, 'room_details.html', {'room': room, 'reservations': reservations})

def book_room(request, id):
    if request.method == 'GET':
        room = Room.objects.get(id=int(id))
        return render(request, 'book_room.html', {"room": room})
    if request.method == 'POST':
        room=Room.objects.get(id=int(id))
        today = datetime.date.today()
        res = request.POST.get('date')
        res_date = datetime.datetime.strptime(res, '%Y-%m-%d').date()
        reservation = Reservation.objects.filter(date=res)
        if not reservation.exists():
            Reservation.objects.create(date=res_date)
        if res_date < today:
            msg = "You can not book room in the past, you ain't doctor Who, my dear"
            return render(request, 'booking_error.html', {"msg": msg})
        elif Reservation.objects.filter(room_booked=room.id, date=res_date).exists():
            msg = 'The room has been already booked on this day'
            return render(request, 'booking_error.html', {'msg': msg})
        else:
            Reservation.objects.get(date=res_date).room_booked.add(Room.objects.get(id=int(id)))
        return HttpResponse('Rezerwacja zrobiona')


def all_rooms(request):
    rooms = Room.objects.all().order_by("id")
    return render(request, 'main_view.html', {'rooms': rooms})

def search_room(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        if request.GET.get('name'):
            rooms = rooms.filter(name__contains=request.GET['name'])
        if request.GET.get('capacity'):
            rooms = rooms.filter(capacity=request.GET['capacity'])
        if request.GET.get('min_capacity'):
            rooms = rooms.filter(capacity__gte=request.GET['min_capacity'])
        if request.GET.get('available'):
            pass
        if request.GET.get('projector'):
            rooms = rooms.filter(projector=True)
        return render(request, 'search_room.html', {'rooms': rooms, 'filters':request.GET})


