from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_room, name='create_room'),
    path('<str:chat_id>/info', views.chat_info, name='chat_info'),
    path('join_room/<str:chat_id>/', views.send_join_request, name='join_request'),
    path('<str:chat_id>/edit', views.edit_chat, name='edit_chat'),
    path('join_room/<str:chat_id>/<int:user_id>', views.handle_join_request, name='handle_join_request'),
    path('<str:chat_id>/<int:user_id>/block', views.block_user, name='block_user'),
    path('<str:chat_id>/<int:user_id>/unblock', views.unblock_user, name='unblock_user'),
    path('delete/<str:chat_id>/', views.delete_chat, name='delete_chat'),
    path('invalid/', views.invalid, name='invalid'),
    path('<str:chat_id>/', views.chat_room, name='chat_room'),
    path('personal/<str:username>/', views.personal_chat_room, name='personal_chat_room'),
]