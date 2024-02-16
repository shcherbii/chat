from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404

from django.http import HttpResponse
import uuid
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .forms import ChatForm
from .models import Chat, ChatMassages, UserPrivareChatRequest, UserChatNotification, ChatUsers, ChatUserType, ChatType

# Generate a random UUID (UUID4)

# Create your views here.

def get_chatuser_type(type):
    return ChatUserType.objects.get(type = type)


def append_user(user):
    chat = Chat.objects.get(id = 1)

    ChatUsers.objects.create(chat = chat, user = user, type = get_chatuser_type('member'))
    

    type_chat = ChatType.objects.get(type = 'personal')
    chat_personal = Chat.objects.create(name = 'personal',  type = type_chat, chat_id = uuid.uuid4().int)

    type_member = get_chatuser_type('member')
    admin = get_object_or_404(User, username = 'admin')

    ChatUsers.objects.create(chat = chat_personal, user = admin, type = type_member)
    ChatUsers.objects.create(chat = chat_personal, user = user, type = type_member)


@login_required
def index(request):    
    return render(request, 'chat/index.html')


@login_required
def send_join_request(request, chat_id):
    if request.method == 'POST':
        chat = get_object_or_404(Chat, chat_id = chat_id)
        if chat.is_private == True:
            room_request = UserPrivareChatRequest(user = request.user, chat = chat)
            room_request.save()
        
    return redirect('index')
    

@login_required
def block_user(request, chat_id, user_id):
    chat = get_object_or_404(Chat, chat_id = chat_id)
    user = get_object_or_404(User, id = user_id)
    chat_user = get_object_or_404(ChatUsers, chat = chat, user = request.user)
    
    if chat_user.type.type == 'creator':


        chat_user_to_block = get_object_or_404(ChatUsers, chat = chat, user = user)

        if chat_user == chat_user_to_block:
            redirect('chat_room', chat.chat_id)
        else:
            if request.method == 'POST':
                chat_user_to_block.status = 'blocked'
                chat_user_to_block.save()

    if chat_user.type.type == 'admin':
        chat = get_object_or_404(Chat, chat_id = chat_id)
        user = get_object_or_404(User, id = user_id)

        chat_user_to_block = get_object_or_404(ChatUsers, chat = chat, user = user)

        if chat_user == chat_user_to_block or chat_user_to_block.type.type == 'creator' or chat_user_to_block.type.type == 'admin':
            redirect('chat_info', chat.chat_id)
        else:
            if request.method == 'POST':
                chat_user_to_block.status = 'blocked'
                chat_user_to_block.save()

    return redirect('chat_info', chat.chat_id)


@login_required
def unblock_user(request, chat_id, user_id):
    chat = get_object_or_404(Chat, chat_id = chat_id)
    user = get_object_or_404(User, id = user_id)
    chat_user = get_object_or_404(ChatUsers, chat = chat, user = request.user)

    if chat_user.type.type == 'creator' or chat_user.type.type == 'admin':

        chat_user_to_block = get_object_or_404(ChatUsers, chat = chat, user = user)

        if chat_user == chat_user_to_block:
            redirect('chat_info', chat.chat_id)
        else:
            if request.method == 'POST':
                chat_user_to_block.status = 'active'
                chat_user_to_block.save()

    return redirect('chat_info', chat.chat_id)


@login_required
def handle_join_request(request, chat_id, user_id):
    chat = get_object_or_404(Chat, chat_id = chat_id)
    user = get_object_or_404(User, id = user_id)

    chat_user = get_object_or_404(ChatUsers, chat = chat, user = request.user)

    if chat_user.type.type == 'admin' or chat_user.type.type == 'creator':
        if request.method == 'POST':
            if request.POST.get('status') == 'accept':

                ChatUsers.objects.create(chat = chat, user = user, type = get_chatuser_type('member'))
                ChatMassages.objects.create(chat = chat, type = 'system', massage_content= f'{user} joined the group')

                room_request = UserPrivareChatRequest.objects.get(chat = chat, user = user)
                
                room_request.request_status = 1
                room_request.save()

            else:
                room_request = UserPrivareChatRequest.objects.get(chat = chat, user = user)
                room_request.request_status = 0
                room_request.save()
        
    return redirect('chat_info', chat.chat_id)


def invalid(request):
    return render(request, 'chat/invalid.html')


@login_required
def create_room(request):

    if request.method == 'POST':
        form = ChatForm(data=request.POST, files=request.FILES)

        if form.is_valid():

            new_room = form.save(commit=False)
            type_chat = ChatType.objects.get(type = 'group')
            new_room.type = type_chat

            new_room.save()

            ChatUsers.objects.create(chat = new_room, user = request.user, type = get_chatuser_type('creator'))
            ChatMassages.objects.create(chat = new_room, type = 'system', massage_content= f'A {new_room.name} group has been created')

            messages.add_message(request, messages.SUCCESS, f"You succsecfuly created  {new_room.name} room.")
            return redirect('index')
    else:
        form = ChatForm(data=request.POST)

    return render(request, 'chat/create.html', {'form': form})


@login_required
def edit_chat(request, chat_id):
    chat = get_object_or_404(Chat, chat_id = chat_id)

    chat_user = get_object_or_404(ChatUsers, chat = chat, user = request.user)
    if chat_user.type.type == 'creator' or chat_user.type.type == 'admin':
        if request.method == 'POST':
            chat_form = ChatForm(instance=chat, data=request.POST, files=request.FILES)

            if chat_form.is_valid():
                print('x')
                chat_form.save()
                

        else:
            chat_form = ChatForm(instance=chat)


        return render(request, 'chat/chat_edit.html', {'chat_form': chat_form})
    else:
        return redirect('invalid')


@login_required
def delete_chat(request, chat_id):
    chat = get_object_or_404(Chat, chat_id = chat_id)
    chat_user = get_object_or_404(ChatUsers, chat = chat, user = request.user)
        
    if chat_user.type.type == 'creator' or chat_user.type.type == 'admin':

        if request.method == 'POST':
            chat.delete()
            messages.add_message(request, messages.SUCCESS, f"You succsecfuly deleted  {chat.name} room.")
            return redirect('index')
        
        return render(request, 'chat/delete.html', {'chat_room': chat})
    else:
        return redirect('invalid')


@login_required
def personal_chat_room(request, username):

    user2 = get_object_or_404(User, username = username)

    # Get the private chat room where both users are present
    private_chat= Chat.objects.filter(
        chatusers__user=request.user,
        chatusers__chat__type__type='personal'
    ).filter(
        chatusers__user=user2,
        chatusers__chat__type__type='personal'
    ).first()

    if private_chat is None:       
        type_chat = ChatType.objects.get(type = 'personal')
        chat = Chat.objects.create(name = 'personal',  type = type_chat, chat_id = uuid.uuid4().int)

        type_member = get_chatuser_type('member')

        ChatUsers.objects.create(chat = chat, user = request.user, type = type_member)
        ChatUsers.objects.create(chat = chat, user = user2, type = type_member)

        return redirect('chat_room', chat.chat_id)
    else:
        return redirect('chat_room', private_chat.chat_id)

    
@login_required
def chat_room(request, chat_id):

    chat_room = get_object_or_404(Chat, chat_id = chat_id)

    UserChatNotification.objects.filter(user = request.user, chat=chat_room).delete() 

    chat_user = ChatUsers.objects.filter(chat = chat_room, user = request.user).first()


    if chat_room.type.type == 'group':       
        if chat_room.is_private:
            if chat_user is None:
                room_request = UserPrivareChatRequest.objects.filter(chat = chat_room, user = request.user)
                if not room_request:
                    return render(request, 'chat/confirm_request.html', {'chatroom': chat_room})
                else:
                    messages.add_message(request, messages.INFO, f"You already send join request to {chat_room.name} room.")
                    return redirect('index')
                
            if chat_user.status == 'blocked': 
                messages.add_message(request, messages.INFO, f"You have been blocked from this chat.")
                return redirect('index')

            chat_messages = ChatMassages.objects.filter(chat = chat_room)

            return render(request, 'chat/room.html', {'chatroom': chat_room, 'room_messages':chat_messages})
        else:
            if chat_user is None:
                ChatUsers.objects.create(chat = chat_room, user = request.user, type = get_chatuser_type('member'))
                ChatMassages.objects.create(chat = chat_room, type = 'system', massage_content= f'{request.user.username} joined the group')
            
            if chat_user.status == 'blocked': 
                messages.add_message(request, messages.INFO, f"You have been blocked from this chat.")
                return redirect('index')

            chat_messages = ChatMassages.objects.filter(chat = chat_room)
            return render(request, 'chat/room.html', {'chatroom': chat_room, 'room_messages':chat_messages})
    
    if chat_room.type.type == 'personal':

        chat_messages = ChatMassages.objects.filter(chat = chat_room)

        return render(request, 'chat/room.html', {'chatroom': chat_room, 'room_messages':chat_messages})


@login_required
def chat_info(request, chat_id):
    chat_room = get_object_or_404(Chat, chat_id = chat_id)
    chat_user = ChatUsers.objects.filter(chat = chat_room, user = request.user).first()
    if chat_user is None:
        messages.add_message(request, messages.INFO, f"You are not a mamber of this group.")
        return redirect('index')
    else:
        if chat_user.type.type == 'creator' or chat_user.type.type == 'admin':
            if chat_room.is_private:

                users_requests = UserPrivareChatRequest.objects.filter(chat = chat_room, request_status = 2)
            else:
                users_requests = None
        else:
            users_requests = False
        active_chat_users = ChatUsers.objects.filter(chat = chat_room, status = 'active')
        blocked_chat_users = ChatUsers.objects.filter(chat = chat_room, status = 'blocked')
        return render(request, 'chat/chat_info.html', {'chatroom': chat_room, 'active_users':active_chat_users, 'blocked_users':blocked_chat_users,"users_requests": users_requests, 'user_type': chat_user.type.type})
    
