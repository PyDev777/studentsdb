# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import AppendedText
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.forms import ModelForm, ValidationError
from ..models import Student, Group
from ..util import paginate, get_current_group

# Views for Students
class StudentUpdateForm(ModelForm):
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
                Submit('save_button', u'Зберегти', css_class='btn btn-primary'),
                Submit('cancel_button', u'Скасувати', css_class='btn btn-default')))
        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})
        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-5'

    def clean_student_group(self):
        """ Check if student is leader in any group
        If yes, then ensure it's the same as selected group. """
        # get group where current student is a leader
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(u'Студент є старостою іншої групи', code='invalid')
        return self.cleaned_data['student_group']


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_add_edit.html'
    form_class = StudentUpdateForm

    def get_context_data(self, **kwargs):
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        context['title'] = u'Редагування студента'
        return context

    def get_success_url(self):
        return u'%s?status_message=Студента успішно збережено!' % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=Редагування студента відмінено!' % reverse('home'))
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
                Submit('save_button', u'Зберегти', css_class='btn btn-primary'),
                Submit('cancel_button', u'Скасувати', css_class='btn btn-default')))
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('students_add')
        self.helper.help_text_inline = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-5'


class StudentAddView(CreateView):
    model = Student
    template_name = 'students/students_add_edit.html'
    form_class = StudentAddForm

    def get_context_data(self, **kwargs):
        context = super(StudentAddView, self).get_context_data(**kwargs)
        context['title'] = u'Додавання студента'
        return context

    def get_success_url(self):
        return u'%s?status_message=Студента успішно збережено!' % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=Додавання студента відмінено!' % reverse('home'))
        else:
            return super(StudentAddView, self).post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        return u'%s?status_message=Студента успішно видалено!' % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=Видалення студента відмінено!' % reverse('home'))
        else:
            return super(StudentDeleteView, self).post(request, *args, **kwargs)


def students_list(request):

    # check if we need to show only one group of students
    current_group = get_current_group(request)
    if current_group:
        students = Student.objects.filter(student_group=current_group)
    else:
        # otherwise show all students
        students = Student.objects.all()

    # try to order students list
    order_by = request.GET.get('order_by', '')
    if order_by not in ('id', 'first_name', 'ticket'):
        order_by = 'last_name'
    students = students.order_by(order_by)

    reverse_by = request.GET.get('reverse', '')
    if reverse_by == '1':
        students = students.reverse()

    # apply pagination, 3 students per page
    context = paginate(students, 3, request, {}, var_name='students')
    context.update({'order_by': order_by, 'reverse': reverse_by, 'students_url': reverse('home')})

    return render(request, 'students/students_list.html', context)
