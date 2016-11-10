# coding: utf-8

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from ..models import Student, Group
from ..util import paginate
from django.utils.translation import ugettext as _


class GroupUpdateForm(ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'leader', 'notes']

    def __init__(self, *args, **kwargs):
        super(GroupUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset('', 'title', 'leader', 'notes'),
            ButtonHolder(
                Submit('save_button', _(u'Save')),
                Submit('cancel_button', _(u'Cancel'), css_class='btn-default')))
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('groups_edit', kwargs={'pk': kwargs['instance'].id})
        self.helper.help_text_inline = False
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-7'

    def clean_leader(self):
        """ Check if (student not in this group) and (student is not None)
        If yes, then ensure it's the same as selected group. """
        # get students in current group
        students = Student.objects.filter(student_group=self.instance)
        if (self.cleaned_data['leader'] not in students) and self.cleaned_data['leader']:
            raise ValidationError(_(u'Student not in this group'), code='invalid')
        return self.cleaned_data['leader']


class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'students/groups_add_edit.html'
    form_class = GroupUpdateForm

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(GroupUpdateView, self).get_context_data(**kwargs)
        context['title'] = _(u'Group edit')
        return context

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('groups'), _(u'Group saved successfully!'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('groups')), _(u'Group update canceled!'))
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs)


class GroupAddForm(ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'leader', 'notes']

    def __init__(self, *args, **kwargs):
        super(GroupAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset('', 'title', 'leader', 'notes'),
            ButtonHolder(
                Submit('save_button', _(u'Save')),
                Submit('cancel_button', _(u'Cancel'), css_class='btn-default')))
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('groups_add')
        self.helper.help_text_inline = False
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-7'


class GroupAddView(CreateView):
    model = Group
    template_name = 'students/groups_add_edit.html'
    form_class = GroupAddForm

    def get_context_data(self, **kwargs):
        context = super(GroupAddView, self).get_context_data(**kwargs)
        context['title'] = _(u'Group add')
        return context

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('groups'), _(u'Group saved successfully!'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('groups')), _(u'Group add cancelled!'))
        else:
            return super(GroupAddView, self).post(request, *args, **kwargs)


class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'))

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('groups'), _(u'Group deleted successfully!'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('groups')), _(u'Group delete canceled!'))
        else:
            return super(GroupDeleteView, self).post(request, *args, **kwargs)


class GroupListView(TemplateView):
    template_name = 'students/groups_list.html'

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        context['groups_url'] = reverse('groups')

        groups = Group.objects.all()
        order_by = self.request.GET.get('order_by', '')
        if order_by not in ('id', 'leader'):
            order_by = 'title'
        groups = groups.order_by(order_by)
        context['order_by'] = order_by

        reverse_by = self.request.GET.get('reverse', '')
        if reverse_by == '1':
            groups = groups.reverse()
        context['reverse'] = reverse_by

        # apply pagination, 2 groups per page
        context.update(paginate(groups, 2, self.request, {}, var_name='groups'))

        return context
