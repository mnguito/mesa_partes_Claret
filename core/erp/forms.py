from datetime import datetime

from django import forms
from django.forms import ModelForm, TextInput, Select, Textarea

from core.erp.models import *


class TipoTramiteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = TipoTramite
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del tipo de trámite',
                    'class': 'form-control',
                }
            ),
        }
        exclude = ['is_active']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TramiteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = TipoTramite
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del tipo de trámite',
                    'class': 'form-control',
                }
            ),
        }
        exclude = ['is_active']
