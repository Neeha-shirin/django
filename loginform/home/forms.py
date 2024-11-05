from django import forms
from .models import Amodel

class Aforms(forms.ModelForm):
    class Meta:
        model = Amodel
        fields = '__all__'  
