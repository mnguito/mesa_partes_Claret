from datetime import datetime

from django import forms
from django.forms import ModelForm, TextInput, Select, Textarea

from core.erp.models import *


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'first_name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre',
                    'required': 'true'
                }
            ),
            'last_name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el apellido',
                    'required': 'true'
                }
            ),
            'document_number': TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'number',
                    'placeholder': 'Ingrese el numero de documento',
                    'required': 'true'
                }
            ),
            'email': TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'email',
                    'placeholder': 'Ingrese su correo electrónico',
                    'required': 'true'
                }
            ),
            'rol': forms.Select(attrs={
                'class': 'custom-select select2',
                'required': 'true'
            }),
        }
        exclude = ['is_active', 'image', 'is_first_time']

    # def save(self, commit=True):
    #     data = {}
    #     form = super()
    #     try:
    #         if form.is_valid():
    #             instance = form.save()
    #             data = instance.toJSON()
    #         else:
    #             data['error'] = form.errors
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return data
