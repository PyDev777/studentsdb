from django import forms
from django.forms import ModelForm, ValidationError, ClearableFileInput
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_view
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, Http404

from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from registration.forms import RegistrationFormUniqueEmail
from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Hidden, Fieldset, ButtonHolder, Layout, HTML
from crispy_forms.bootstrap import AppendedText
from .models import StProfile


# Create your views here.


class CustRegFormUniqEmail(RegistrationFormUniqueEmail):

    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(CustRegFormUniqEmail, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse('users:registration_register')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.error_text_inline = False
        self.helper.add_input(Submit('submit_button', _(u'Register')))
        self.helper.add_input(Button('cancel_button', _(u'Cancel'), css_class='btn-default'))


class CustAuthForm(AuthenticationForm):

    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(CustAuthForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse('users:auth_login')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-9'
        self.helper.error_text_inline = False
        self.helper.layout = Layout(
            Hidden('next', value=reverse('home')),
            Fieldset('', 'username', 'password',
                     HTML(u"<strong><a href='%s' class='btn btn-link col-sm-offset-3 modal-link'>%s</a></strong>" % (reverse('password_reset'), _(u'Forgot your password?'))),
                     'captcha'),
            ButtonHolder(Submit('submit_button', _(u'Log in')),
                         Button('cancel_button', _(u'Cancel'), css_class='btn-default')))


class CustPswResetForm(PasswordResetForm):

    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(CustPswResetForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse('password_reset')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.error_text_inline = False
        self.helper.add_input(Submit('submit_button', _(u'Confirm')))
        self.helper.add_input(Button('cancel_button', _(u'Cancel'), css_class='btn-default'))

        # self.helper.layout = Layout(
        #     # Hidden('next', value=reverse('home')),
        #     HTML(u"<p>%s</p>" % _(u"Forgot your password? Enter your email in the form below and we'll send you instructions for creating a new one.")),
        #     Fieldset('', 'email', 'captcha'),
        #     ButtonHolder(Submit('submit_button', _(u'Confirm')),
        #                  Button('cancel_button', _(u'Cancel'), css_class='btn-default')))


class CustSetPswForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(CustSetPswForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.error_text_inline = False
        self.helper.layout = Layout(
            HTML(u"<p>%s</p>" % _(u"Enter your new password below to reset your password:")),
            Fieldset('', 'new_password1', 'new_password2'),
            ButtonHolder(Submit('submit_button', _(u'Confirm')),
                         Button('cancel_button', _(u'Cancel'), css_class='btn-default')))


class CustPswChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(CustPswChangeForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse('auth_password_change')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.error_text_inline = False
        self.helper.add_input(Submit('submit_button', _(u'Confirm')))
        self.helper.add_input(Button('cancel_button', _(u'Cancel'), css_class='btn-default'))


class ImageViewFileInput(ClearableFileInput):

    def render(self, name, value, attrs=None):
        html = super(ImageViewFileInput, self).render(name, value, attrs)
        if value and hasattr(value, 'url'):
            img_html = mark_safe('<img src="%s" class="img-circle" height="30" width="30"><br>' % value.url)
            html = img_html + html
        return html


class ProfileForm(ModelForm):
    photo = forms.ImageField(widget=ImageViewFileInput(), required=False, label=_(u"Photo"))

    class Meta:
        model = StProfile
        fields = ['photo', 'birthday', 'mobile_phone', 'address']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse('profile')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-9'
        self.helper.help_text_inline = False
        self.helper.layout = Layout(
            Fieldset('', 'photo',
                     AppendedText('birthday', '<span class="glyphicon glyphicon-calendar"></span>'),
                     'mobile_phone', 'address'),
            ButtonHolder(
                Submit('save_button', _(u'Save')),
                Submit('cancel_button', _(u'Cancel'), css_class='btn-default')))

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if photo and (len(photo) > 500000):
            raise ValidationError(_(u'Maximum size - 500Kb!'), code='invalid')
        return photo


class ProfileView(UpdateView):
    model = StProfile
    template_name = 'profile.html'
    form_class = ProfileForm

    def get_object(self, queryset=None):
        obj, created = self.model.objects.get_or_create(user=self.request.user)
        return obj

    def get_success_url(self):
        # messages.success(self.request, (_(u'Student updated successfully!') + ' (%s)' % self.object.__unicode__()))
        return HttpResponseRedirect(reverse('home'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            # messages.warning(self.request, _(u'Student update canceled!'))
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(ProfileView, self).post(request, *args, **kwargs)


def custom_password_reset_confirm(request, uidb64=None, token=None):
    if request.is_ajax():
        return auth_view.password_reset_confirm(request, uidb64, token, set_password_form=CustSetPswForm)
    else:
        return render(request, 'registration/form_redirect.html', {'form_url': request.build_absolute_uri()})


# def custom_activation_complete(request):
#     print 'custom_activation_complete'
#     return render(request, 'registration/activation_complete.html', {})
