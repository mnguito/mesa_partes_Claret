from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.user.choices import active_states_choices


class Rol(models.Model):
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
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['id']


class User(AbstractUser):
    document_number = models.CharField(max_length=100, blank=True, null=True, verbose_name='Número de Documento')
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Rol')
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)
    is_first_time = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return str(self.first_name + " " + self.last_name)

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        if self.rol:
            item['rol'] = self.rol.toJSON()
        else:
            item['rol'] = {"name": "--"}
        item['image'] = str(self.first_name + " " + self.last_name)
        return item
