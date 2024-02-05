from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('my/', views.get_user_rooms, name='my_rooms'),
    path('create/', views.create_room, name='create_room'),
    path('room_users/<str:uniqe_key>/', views.room_users_list, name='room_users'),
    path('join_room/<str:uniqe_key>/', views.send_join_request, name='join_request'),
    path('join_room/<str:uniqe_key>/<int:user_id>', views.handle_join_request, name='handle_join_request'),
    path('delete/<str:uniqe_key>/', views.delete_room, name='delete_room'),
    path('invalid/', views.invalid, name='invalid'),
    path('<str:uniqe_key>/', views.chat_room, name='chat_room'),
]