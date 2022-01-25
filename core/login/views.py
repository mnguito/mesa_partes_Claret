from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView

import config.settings as setting

from django.db.models import Q
# from core.erp.models import *
from core.user.models import *


def renderLogin(request):
    template_name = 'login.html'

    if request.POST:
        dataFromHTML = request.POST
        username = dataFromHTML['username']
        password = dataFromHTML['password']
        if User.objects.filter(Q(username=username)).exists():
            user = User.objects.get(Q(username=username))
            if user.is_active:
                if user.check_password(password):
                    registered_user = authenticate(request, username=username, password=password)
                    if registered_user is not None:  # Succesful login
                        login(request, registered_user)
                        return redirect('erp:dashboard')
                    else:  # Unsuccesul login
                        context = {
                            'failLogin': 1
                        }
                        return render(request, template_name, context)
                else:  # Unsuccesul login
                    context = {
                        'failLogin': 1,
                        'error_message': 'La contraseña es incorrecta.'
                    }
                    return render(request, template_name, context)
            else:  # Unsuccesul login
                if user.is_first_time:
                    context = {
                        'firstTime': 1,
                        'title_page': 'Login',
                        'error_message': 'Es su primera vez ingresando, primero cambie su contraseña.'
                    }
                    return render(request, template_name, context)
                else:
                    context = {
                        'failLogin': 1,
                        'title_page': 'Login',
                        'error_message': 'El usuario no está activo. Por favor, comunicarse con el Administrador.'
                    }
                    return render(request, template_name, context)
        else:  # Unsuccesul login
            context = {
                'failLogin': 1,
                'error_message': 'El usuario es incorrecto.'
            }
            return render(request, template_name, context)
    else:
        if request.user.is_authenticated:
            registered_user = request.user
            return redirect('erp:dashboard')
        else:
            context = {
                'failLogin': 0,
                'title_page': 'Login',
                'is_active_login': 'active'
            }
            return render(request, template_name, context)


def renderPassword(request):
    template_name_login = 'login.html'
    template_name_out = 'change_password_out.html'
    template_name_in = 'change_password_in.html'

    if request.POST:
        if not request.user.is_authenticated:
            dataFromHTML = request.POST
            username = dataFromHTML['username']
            old_password = dataFromHTML['old_password']
            new_password = dataFromHTML['new_password']
            confirm_new_password = dataFromHTML['confirm_new_password']

            if User.objects.filter(Q(username=username)).exists():
                user = User.objects.get(Q(username=username))
                if user.is_first_time:
                    if user.check_password(old_password):
                        if old_password != new_password:
                            if new_password == confirm_new_password:
                                user.set_password(new_password)
                                user.is_first_time = False
                                user.is_active = True
                                user.save()
                                context = {
                                    'flagChangeFail': 0,
                                    'flagChangeSuccess': 1,
                                    'success_message': 'La contraseña se cambio exitosamente'
                                }
                                return render(request, template_name_out, context)
                            else:  # Unsuccesul change
                                context = {
                                    'flagChangeFail': 1,
                                    'flagChangeSuccess': 0,
                                    'error_message': 'La contraseña nueva no es igual a la confirmación de contraseña'
                                }
                                return render(request, template_name_out, context)
                        else:  # Unsuccesul change
                            context = {
                                'flagChangeFail': 1,
                                'flagChangeSuccess': 0,
                                'error_message': 'La contraseña nueva no debe ser igual a la actual'
                            }
                            return render(request, template_name_out, context)

                    else:  # Unsuccesul change
                        context = {
                            'flagChangeFail': 1,
                            'flagChangeSuccess': 0,
                            'error_message': 'La contraseña actual es incorrecta.'
                        }
                        return render(request, template_name_out, context)
                else:  # Unsuccesul change
                    if user.is_active:
                        context = {
                            'flagChangeFail': 1,
                            'flagChangeSuccess': 0,
                            'error_message': 'Ingrese a su intranet y cambie la contraseña desde su perfil'
                        }
                        return render(request, template_name_out, context)
                    else:
                        context = {
                            'flagChangeFail': 1,
                            'flagChangeSuccess': 0,
                            'error_message': 'El usuario no está activo. Por favor, comunicarse con el Administrador.'
                        }
                        return render(request, template_name_out, context)
            else:  # Unsuccesul change
                context = {
                    'flagChangeFail': 1,
                    'flagChangeSuccess': 0,
                    'error_message': 'El usuario es incorrecto.'
                }
                return render(request, template_name_out, context)
        else:
            dataFromHTML = request.POST
            old_password = dataFromHTML['old_password']
            new_password = dataFromHTML['new_password']
            confirm_new_password = dataFromHTML['confirm_new_password']

            if request.user.check_password(old_password):
                if old_password != new_password:
                    if new_password == confirm_new_password:
                        request.user.set_password(new_password)
                        request.user.save()
                        registered_user = authenticate(request, username=request.user.username,
                                                       password=request.user.password)
                        login(request, registered_user)
                        context = {
                            'flagChangeFail': 0,
                            'flagChangeSuccess': 1,
                            'success_message': 'La contraseña se cambio exitosamente'
                        }
                        return render(request, template_name_in, context)
                    else:  # Unsuccesul change
                        context = {
                            'flagChangeFail': 1,
                            'flagChangeSuccess': 0,
                            'error_message': 'La contraseña nueva no es igual a la confirmación de contraseña'
                        }
                        return render(request, template_name_in, context)
                else:  # Unsuccesul change
                    context = {
                        'flagChangeFail': 1,
                        'flagChangeSuccess': 0,
                        'error_message': 'La contraseña nueva no debe ser igual a la actual'
                    }
                    return render(request, template_name_in, context)
            else:  # Unsuccesul change
                context = {
                    'flagChangeFail': 1,
                    'flagChangeSuccess': 0,
                    'error_message': 'La contraseña actual es incorrecta.'
                }
                return render(request, template_name_in, context)
    else:
        if request.user.is_authenticated:
            context = {
                'flagChangeFail': 0,
                'flagChangeSuccess': 0,
                'title_page': 'Change Password'
            }
            return render(request, template_name_in, context)
        else:
            context = {
                'flagChangeFail': 0,
                'flagChangeSuccess': 0,
                'title_page': 'Change Password'
            }
            return render(request, template_name_out, context)


class LoginFormView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context


class LoginFormView2(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context


class LogoutView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)
