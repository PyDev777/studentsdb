from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationFormUniqueEmail
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Hidden, Fieldset, ButtonHolder, Layout, HTML, Div


class CustomRegistrationFormUniqueEmail(RegistrationFormUniqueEmail):

    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(CustomRegistrationFormUniqueEmail, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse('users:registration_register')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.error_text_inline = False
        self.helper.add_input(Submit('submit_button', _(u'Register')))
        self.helper.add_input(Button('cancel_button', _(u'Cancel'), css_class='btn-default'))


class CustomAuthenticationForm(AuthenticationForm):

    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

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


class CustomPasswordResetForm(PasswordResetForm):

    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)

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


class CustomSetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.error_text_inline = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            HTML(u"<p>%s</p>" % _(u"Enter your new password below to reset your password:")),
            Fieldset('', 'new_password1', 'new_password2'),
            ButtonHolder(Submit('submit_button', _(u'Confirm')),
                         Button('cancel_button', _(u'Cancel'), css_class='btn-default')))


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse('auth_password_change')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.error_text_inline = False
        self.helper.add_input(Submit('submit_button', _(u'Confirm')))
        self.helper.add_input(Button('cancel_button', _(u'Cancel'), css_class='btn-default'))
