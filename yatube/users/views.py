from django.contrib.auth.forms import (AuthenticationForm,
                                       PasswordChangeForm,
                                       PasswordResetForm,
                                       SetPasswordForm
                                       )
from django.contrib.auth.views import (LoginView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView
                                       )
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class Login(LoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/login.html'


class PasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'


class PasswordReset(PasswordResetView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')
    template_name = 'users/password_reset_form.html'


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url = reverse_lazy('users:password_reset_compete')
    template_name = 'users/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
