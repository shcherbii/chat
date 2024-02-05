from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404

from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import RoomCreateForm
from .models import ChatRoom, ChatMassages, UserPrivareRoomRequest

# Generate a random UUID (UUID4)

# Create your views here.

def index(request):    
    # chat_rooms = ChatRoom.objects.filter(type__type = 'public')
    chat_rooms = ChatRoom.objects.all()

    # if request.user.is_authenticated:
    #     users_requests = UserPrivareRoomRequest.objects.filter(room__creator = request.user, request_status =2)
    # else:
    #     users_requests = None

    # return render(request, 'chat/index.html', {'chatrooms': chat_rooms, 'users_requests': users_requests})
    return render(request, 'chat/index.html', {'chatrooms': chat_rooms})



@login_required
def get_user_rooms(request):
    chat_rooms = ChatRoom.objects.filter(creator__id = request.user.id)
    return render(request, 'chat/my_rooms.html', {'chatrooms': chat_rooms})


@login_required
def send_join_request(request, uniqe_key):
    if request.method == 'POST':
        room = get_object_or_404(ChatRoom, uniqe_key = uniqe_key)
        if room.type.type == 'private':
            room_request = UserPrivareRoomRequest(user = request.user, room = room)
            room_request.save()

            return redirect('index')
        
    return redirect('index')
    

def invalid(request):
    return render(request, 'myapp/invalid.html')


@login_required
def handle_join_request(request, uniqe_key, user_id):
    room = get_object_or_404(ChatRoom, uniqe_key = uniqe_key)
    user = get_object_or_404(User, id = user_id)

    if room.creator == request.user:
        if request.method == 'POST':
            if request.POST.get('status') == 'accept':
                room.room_user.add(user)
                room_request = UserPrivareRoomRequest.objects.get(room = room, user = user)
                room_request.request_status = 1
                room_request.save()
                return redirect('index')
            else:
                room_request = UserPrivareRoomRequest.objects.get(room = room, user = user)
                room_request.request_status = 0
                room_request.save()
                return redirect('index')

        return redirect('index')
        
    return redirect('index')
    

def invalid(request):
    return render(request, 'myapp/invalid.html')


@login_required
def delete_room(request, uniqe_key):
    chat_room = ChatRoom.objects.get(uniqe_key = uniqe_key)

    if chat_room.creator != request.user:
        return redirect('invalid')
    
    if request.method == 'POST':
        chat_room.delete()
        return redirect('my_rooms')
    
    return render(request, 'chat/delete.html', {'chat_room': chat_room})



@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomCreateForm(data=request.POST)
        if form.is_valid():
            new_room = form.save(commit=False)
            new_room.creator = request.user
            new_room.save()
            messages.add_message(request, messages.SUCCESS, f"You succsecfuly created  {new_room.name} room.")
            return redirect('index')
    else:
        form = RoomCreateForm(data=request.POST)


    return render(request, 'chat/create.html', {'form': form})


@login_required
def chat_room(request, uniqe_key):

    chat_room = ChatRoom.objects.get(uniqe_key = uniqe_key)

    if chat_room.type.type == 'public':
        chat_messages = ChatMassages.objects.filter(room = chat_room)
        print('x')
        if chat_room.creator != request.user and not request.user in chat_room.room_user.all():
             chat_room.room_user.add(request.user)

        return render(request, 'chat/room.html', {'chatroom': chat_room, 'room_messages':chat_messages})
    
    if chat_room.type.type == 'private':
        if chat_room.creator == request.user:
            chat_messages = ChatMassages.objects.filter(room = chat_room)
            return render(request, 'chat/room.html', {'chatroom': chat_room, 'room_messages':chat_messages})
        elif  request.user in chat_room.room_user.all():
            chat_messages = ChatMassages.objects.filter(room = chat_room)
            return render(request, 'chat/room.html', {'chatroom': chat_room, 'room_messages':chat_messages})
        else:
            room_request = UserPrivareRoomRequest.objects.filter(room = chat_room, user = request.user)
            if not room_request:
                return render(request, 'chat/confirm_request.html', {'chatroom': chat_room})
            else:
                messages.add_message(request, messages.INFO, f"You already send join request to {chat_room.name} room.")
                return redirect('index')
    

@login_required
def room_users_list(request, uniqe_key):
    room = get_object_or_404(ChatRoom, uniqe_key = uniqe_key)

    if request.user == room.creator:
        return render(request, 'chat/chat_users.html', {'chatroom': room})
    else:
        messages.add_message(request, messages.INFO, f"You are not creator of {chat_room.name} room!")
        return redirect('index')
