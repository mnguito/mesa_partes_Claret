from django.urls import path

from core.login.views import *

urlpatterns = [
    path('', renderLogin, name='login'),
    # path('', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('logout/', LogoutRedirectView.as_view(), name='logout')
    path('change_password', renderPassword, name="change_password"),
]
