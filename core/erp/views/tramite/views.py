from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import TipoTramiteForm, TramiteForm
from core.erp.mixins import ValidatePermissionRequiredMixin, ValidateUserStaff
from core.erp.models import TipoTramite, Tramite


class TramiteListView(LoginRequiredMixin, ListView):
    model = TipoTramite
    template_name = 'tramite/list.html'

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
                for i in Tramite.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Trámites'
        context['create_url'] = reverse_lazy('erp:tramite_create')
        context['list_url'] = reverse_lazy('erp:tramite_list')
        context['entity'] = 'Trámites'
        return context


def tramite_create(request):
    template_name = 'tramite/create.html'

    if request.POST:
        dataFromHTML = request.POST
    else:
        context = {
            'title': 'Crear Trámite',
            'action': 'add',
            'list_url': reverse_lazy('erp:tramite_list')
        }
        return render(request, template_name, context)
