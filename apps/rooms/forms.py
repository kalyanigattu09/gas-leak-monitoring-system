from django import forms

from .models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Room name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
