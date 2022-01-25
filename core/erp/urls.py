from django.urls import path

from core.erp.views.dashboard.views import *
from core.erp.views.tipo_tramite.views import *
from core.erp.views.tramite.views import *

app_name = 'erp'

urlpatterns = [
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('procesos/tipo_tramite/list/', TipoTramiteListView.as_view(), name='tipo_tramite_list'),
    path('procesos/tipo_tramite/add/', TipoTramiteCreateView.as_view(), name='tipo_tramite_create'),
    path('procesos/tipo_tramite/delete/<int:pk>/', TipoTramiteDeleteView.as_view(), name='tipo_tramite_delete'),
    path('procesos/tipo_tramite/update/<int:pk>/', TipoTramiteUpdateView.as_view(), name='tipo_tramite_update'),

    path('procesos/tramite/list/', TramiteListView.as_view(), name='tramite_list'),
    path('procesos/tramite/add/', tramite_create, name='tramite_create'),
]
