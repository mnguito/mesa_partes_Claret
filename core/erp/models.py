from django.db import models
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import *
from core.models import BaseModel
from core.user.models import User


class TipoTramite(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nombre')
    is_active = models.CharField(max_length=80, choices=active_states_choices, default='1', blank=True, null=True,
                                 verbose_name='Estado')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['is_active'] = {'id': self.is_active, 'name': self.get_is_active_display()}
        return item

    class Meta:
        verbose_name = 'Tipo de Trámite'
        verbose_name_plural = 'Tipos de Trámites'
        ordering = ['id']


class Tramite(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL, verbose_name='Usuario')
    tipo = models.ForeignKey(TipoTramite, on_delete=models.SET_NULL, blank=True, null=True,
                             verbose_name='Tipo de Trámite')
    address = models.CharField(max_length=3000, blank=True, null=True, verbose_name='Dirección')
    phone = models.IntegerField(blank=True, null=True, verbose_name='Teléfono')
    document_number = models.IntegerField( blank=True, null=True, verbose_name='Número de Documento')
    folio_number = models.IntegerField( blank=True, null=True, verbose_name='Número de Folio')
    subject = models.CharField(max_length=3000, blank=True, null=True, verbose_name='Asunto')
    archivo = models.FileField(upload_to='tramite/archivo', blank=True, null=True, verbose_name='Archivo')
    observation = models.CharField(max_length=5000, blank=True, null=True, verbose_name='Observación')
    state = models.CharField(max_length=80, choices=active_states_choices, default='1', blank=True, null=True,
                             verbose_name='Estado')
    date_creation = models.DateTimeField(auto_now=True, verbose_name='Fecha de Creación')
    date_updated = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Actualización')

    def __str__(self):
        return self.subject

    def get_file(self):
        if self.archivo:
            return '{}{}'.format(MEDIA_URL, self.archivo)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['date_creation'] = self.date_creation.strftime('%Y-%m-%d')
        item['date_updated'] = self.date_updated.strftime('%Y-%m-%d')
        item['user'] = str(self.user.first_name + " " + self.user.last_name)
        item['tipo'] = self.tipo.toJSON()
        item['archivo'] = self.get_file()
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        return item

    class Meta:
        verbose_name = 'Trámite'
        verbose_name_plural = 'Trámites'
        ordering = ['id']
