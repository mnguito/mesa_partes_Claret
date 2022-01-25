from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.erp.mixins import ValidatePermissionRequiredMixin, ValidateUserStaff


# class DashboardView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        return context
