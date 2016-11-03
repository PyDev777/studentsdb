from django.shortcuts import render
from django.contrib.auth import views as auth_view
from stud_auth.forms import CustomSetPasswordForm
from registration.backends.default.views import ActivationView

# Create your views here.


def custom_password_reset_confirm(request, uidb64=None, token=None):
    if request.is_ajax():
        return auth_view.password_reset_confirm(request, uidb64, token, set_password_form=CustomSetPasswordForm)
    else:
        return render(request, 'registration/form_redirect.html', {'form_url': request.build_absolute_uri()})


def custom_activation_complete(request):
    print 'custom_activation_complete'
    return render(request, 'registration/activation_complete.html', {})
