from django import forms
from .models import ChatRoom

class RoomCreateForm(forms.ModelForm):

    class Meta:
        model = ChatRoom
        fields = ('name', 'type')