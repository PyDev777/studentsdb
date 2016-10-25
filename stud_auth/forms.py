from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationFormUniqueEmail
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Hidden, Fieldset, ButtonHolder, Layout, Div, HTML


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
        self.helper.add_input(Submit('register_button', _(u'Register')))
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
                     Button('forgot_button', _(u'Forgot your password?'), css_class='btn-link btn-xs col-sm-offset-3'),
                     HTML('<p></p>'),
                     'captcha'),
            ButtonHolder(Submit('login_button', _(u'Save')),
                         Button('cancel_button', _(u'Cancel'), css_class='btn-default')))
