# coding: utf-8

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from studentsdb.settings import ADMIN_EMAIL, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_USE_SSL
from django import forms
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit


class ContactLetterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # call original initializator
        super(ContactLetterForm, self).__init__(*args, **kwargs)

        # this helper object allows us to customize form
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Fieldset('', 'from_email', 'subject', 'message'),
            ButtonHolder(
                Submit('save_button', u'Надіслати'),
                Submit('cancel_button', u'Скасувати')))

        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact_letter')

        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.label_class = 'col-sm-4 control-label'
        self.helper.field_class = 'col-sm-7'

    from_email = forms.EmailField(
        label=u"Ваша Емейл Адреса",
        required=True)

    subject = forms.CharField(
        label=u"Заголовок листа",
        max_length=128,
        required=True)

    message = forms.CharField(
        label=u"Текст повідомлення",
        max_length=2560,
        widget=forms.Textarea,
        required=True)


class ContactLetterView(FormView):
    template_name = 'contact_admin/contact_form.html'
    form_class = ContactLetterForm

    def get_context_data(self, **kwargs):
        context = super(ContactLetterView, self).get_context_data(**kwargs)
        context['title'] = u"Зв'язок з Адміністратором"
        return context

    def form_valid(self, form):
        # send email
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        from_email = form.cleaned_data['from_email']
        try:
            send_mail(from_email + ' send me: ' + subject, message, EMAIL_HOST_USER, [ADMIN_EMAIL])
            # pass
            # if True:
            #     raise Exception
        except Exception:
            message = u'Під час відправки листа виникла непередбачувана помилка. ' \
                        u'Спробуйте скористатись даною формою пізніше.'
            message_error = '1'
            return HttpResponseRedirect(u'%s?status_message=%s&message_error=%s' % (reverse('contact_admin'), message, message_error))
        else:
            message = u'Повідомлення успішно надіслане!'
            # redirect to same contact page with success message
            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('contact_admin'), message))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=Відправу листа відмінено!' % reverse('contact_admin'))
        else:
            return super(ContactLetterView, self).post(request, *args, **kwargs)


class ContactAdminView(TemplateView):
    template_name = 'contact_admin/contact_page.html'

    def get_context_data(self, **kwargs):
        context = super(ContactAdminView, self).get_context_data(**kwargs)
        context['contact_url'] = reverse('contact_admin')
        return context
