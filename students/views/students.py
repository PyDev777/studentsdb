# coding: utf-8

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import AppendedText
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django import forms
from django.forms import ModelForm, ValidationError
from django.utils.safestring import mark_safe
from django.forms import ClearableFileInput
from ..models import Student, Group
from ..util import paginate, get_current_group
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy


class ImageViewFileInput(ClearableFileInput):

    def render(self, name, value, attrs=None):
        html = super(ImageViewFileInput, self).render(name, value, attrs)
        if value and hasattr(value, 'url'):
            img_html = mark_safe('<img src="%s" class="img-circle" height="30" width="30"><br>' % value.url)
            html = img_html + html
        return html


class StudentUpdateForm(ModelForm):
    photo = forms.ImageField(widget=ImageViewFileInput(), required=False, label=ugettext_lazy(u"Photo"))

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'middle_name', 'birthday', 'photo', 'ticket', 'student_group', 'notes']

    def __init__(self, *args, **kwargs):
        # call original initialization
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        # this helper object allows us to customize form
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset('', 'first_name', 'last_name', 'middle_name',
                     AppendedText('birthday', '<span class="glyphicon glyphicon-calendar"></span>'),
                     'photo', 'ticket', 'student_group', 'notes'),
            ButtonHolder(
                Submit('save_button', _(u'Save')),
                Submit('cancel_button', _(u'Cancel'))))

        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})

        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.label_class = 'col-sm-4 control-label'
        self.helper.field_class = 'col-sm-7'

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if photo and (len(photo) > 500000):
            raise ValidationError(_(u'Maximum size - 500Kb!'), code='invalid')
        return photo

    def clean_student_group(self):
        """ Check if student is leader in any group
        If yes, then ensure it's the same as selected group. """
        # get group where current student is a leader
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(_(u'Student is the leader of another group!'), code='invalid')
        return self.cleaned_data['student_group']


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_add_edit.html'
    form_class = StudentUpdateForm

    # def dispatch(self, *args, **kwargs):
    #     get_object_or_404(Student, pk=kwargs['pk'])
    #     return super(StudentUpdateView, self).dispatch(*args, **kwargs)

    # def get_object(self, queryset=None):
    #     try:
    #         obj = self.model.objects.get(pk=self.kwargs.get('pk'))
    #     except self.model.DoesNotExist:
    #         raise Http404
    #     return obj

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        context['title'] = _(u'Student edit')
        return context

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('home'), _(u'Student updated successfully!'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('home'), _(u'Student update canceled!')))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)


class StudentAddForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'middle_name', 'birthday', 'photo', 'ticket', 'student_group', 'notes']

    def __init__(self, *args, **kwargs):
        super(StudentAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Fieldset('', 'first_name', 'last_name', 'middle_name',
                     AppendedText('birthday', '<span class="glyphicon glyphicon-calendar"></span>'),
                     'photo', 'ticket', 'student_group', 'notes'),
            ButtonHolder(
                Submit('save_button', _(u'Save')),
                Submit('cancel_button', _(u'Cancel'))))

        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('students_add')

        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.label_class = 'col-sm-4 control-label'
        self.helper.field_class = 'col-sm-7'

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if photo and (len(photo) > 500000):
            raise ValidationError(_(u'Maximum size - 500Kb!'), code='invalid')
        return photo


class StudentAddView(CreateView):
    model = Student
    template_name = 'students/students_add_edit.html'
    form_class = StudentAddForm

    def get_context_data(self, **kwargs):
        context = super(StudentAddView, self).get_context_data(**kwargs)
        context['title'] = _(u'Student add')
        return context

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('home'), _(u'Student added successfully!'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('home')), _(u'Student addition canceled!'))
        else:
            return super(StudentAddView, self).post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'))

    def get_success_url(self):
        return u'%s?status_message=%s' % (reverse('home'), _(u'Student deleted successfully!'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('home')), _(u'Student deletion canceled!'))
        else:
            return super(StudentDeleteView, self).post(request, *args, **kwargs)


class StudentListView(TemplateView):
    template_name = 'students/students_list.html'

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        context['students_url'] = reverse('home')

        current_group = get_current_group(self.request)
        if current_group:
            students = Student.objects.filter(student_group=current_group)
        else:
            # otherwise show all students
            students = Student.objects.all()

        order_by = self.request.GET.get('order_by', '')
        if order_by not in ('id', 'first_name', 'ticket'):
            order_by = 'last_name'
        students = students.order_by(order_by)
        context['order_by'] = order_by

        reverse_by = self.request.GET.get('reverse', '')
        if reverse_by == '1':
            students = students.reverse()
        context['reverse'] = reverse_by

        # apply pagination, 3 students per page
        context.update(paginate(students, 3, self.request, {}, var_name='students'))

        return context
