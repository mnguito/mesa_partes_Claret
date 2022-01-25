from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import TipoTramiteForm
from core.erp.mixins import ValidatePermissionRequiredMixin, ValidateUserStaff
from core.erp.models import TipoTramite


class TipoTramiteListView(LoginRequiredMixin, ListView):
    model = TipoTramite
    template_name = 'tipo_tramite/list.html'

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
                for i in TipoTramite.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Tipos de Trámites'
        context['create_url'] = reverse_lazy('erp:tipo_tramite_create')
        context['list_url'] = reverse_lazy('erp:tipo_tramite_list')
        context['entity'] = 'Tipos de Trámites'
        return context


class TipoTramiteCreateView(LoginRequiredMixin, CreateView):
    model = TipoTramite
    form_class = TipoTramiteForm
    template_name = 'tipo_tramite/create.html'
    success_url = reverse_lazy('erp:tipo_tramite_list')
    # permission_required = 'erp.add_client'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación un Tipo de Trámite'
        context['entity'] = 'Tipos de Trámites'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class TipoTramiteUpdateView(LoginRequiredMixin, UpdateView):
    model = TipoTramite
    form_class = TipoTramiteForm
    template_name = 'tipo_tramite/create.html'
    success_url = reverse_lazy('erp:tipo_tramite_list')
    # permission_required = 'erp.change_client'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Tipo de Trámite'
        context['entity'] = 'Tipos de Trámites'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class TipoTramiteDeleteView(LoginRequiredMixin, DeleteView):
    model = TipoTramite
    template_name = 'tipo_tramite/delete.html'
    success_url = reverse_lazy('erp:tipo_tramite_list')
    # permission_required = 'erp.delete_office_client'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            tipo_tramite = self.get_object()
            tipo_tramite.is_active = 0
            tipo_tramite.save()
            # self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Tipo de Trámite'
        context['entity'] = 'Tipos de Trámites'
        context['list_url'] = self.success_url
        return context
