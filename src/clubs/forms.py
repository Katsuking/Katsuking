from django import forms
from .models import Club

class ClubsDataForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = '__all__'