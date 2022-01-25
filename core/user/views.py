from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.mixins import ValidatePermissionRequiredMixin, ValidateUserStaff
from core.user.forms import UserForm
from core.user.models import User
from django.contrib.auth.models import Group


class UserListView(LoginRequiredMixin,  ListView):
    model = User
    template_name = 'user/list.html'

    # permission_required = 'erp.view_client'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in User.objects.filter(is_active=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Usuarios'
        context['create_url'] = reverse_lazy('user:user_create')
        context['list_url'] = reverse_lazy('user:user_list')
        context['entity'] = 'Usuarios'
        return context


class UserCreateView(LoginRequiredMixin,  CreateView):
    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('user:user_list')
    # permission_required = 'erp.add_client'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                with transaction.atomic():
                    if request.user.is_superuser:
                        user = json.loads(request.POST['user'])
                        first_name = user['first_name']
                        last_name = user['last_name']
                        rol = user['rol']
                        document_number = user['document_number']
                        email = user['email']
                        password = user['document_number']
                        confirmPassword = user['document_number']
                        if password == confirmPassword:
                            if not User.objects.filter(email=email).exists():  # No existing user
                                user = User.objects.create_user(first_name=first_name, last_name=last_name,
                                                                username=email, document_number=document_number,
                                                                rol_id=rol, is_active=False, password=password,
                                                                email=email, is_staff=False)
                                # group = Group.objects.get(name="Admin")
                                # group.user_set.add(user)
                                data = {'id': user.id}
                            else:  # Already existing user
                                data['error'] = 'Correo electronico ingresado ya en uso'
                        else:
                            data['error'] = 'No coinciden las contraseñas'
                    else:
                        data['error'] = 'No tiene permiso para crear usuario'
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
            return JsonResponse(data)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class UserUpdateView(LoginRequiredMixin,  UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('user:user_list')
    # permission_required = 'erp.change_client'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # if action == 'edit':
            # with transaction.atomic():
            #     if request.user.is_superuser:
            #         user_post = json.loads(request.POST['user'])
            #         user = self.get_object()
            #         user.first_name = user_post['first_name']
            #         user.last_name = user_post['last_name']
            #         user.rol = user_post['rol']
            #         user.document_number = user_post['document_number']
            #         user.email = user_post['email']
            #         user.password = user_post['document_number']
            #         confirmPassword = user_post['document_number']
            #         if password == confirmPassword:
            #             if not User.objects.filter(email=email).exists():  # No existing user
            #                 user = User.objects.create_user(first_name=first_name, last_name=last_name,
            #                                                 username=email, document_number=document_number,
            #                                                 rol_id=rol, is_active=False, password=password,
            #                                                 email=email, is_staff=False)
            #                 # group = Group.objects.get(name="Admin")
            #                 # group.user_set.add(user)
            #                 data = {'id': user.id}
            #             else:  # Already existing user
            #                 data['error'] = 'Correo electronico ingresado ya en uso'
            #         else:
            #             data['error'] = 'No coinciden las contraseñas'
            #     else:
            #         data['error'] = 'No tiene permiso para crear usuario'
            # else:
            #     data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
            return JsonResponse(data)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = []
        context['rol_id'] = self.get_object().rol.id
        return context


class UserDeleteView(LoginRequiredMixin,  DeleteView):
    model = User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user:user_list')
    # permission_required = 'erp.delete_client'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            user = self.get_object()
            user.is_active = False
            user.save()
            # self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Cliente'
        context['entity'] = 'Clientes'
        context['list_url'] = self.success_url
        return context
