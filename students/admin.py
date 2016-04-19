# coding: utf-8

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError
from .models import Student, Group, MonthJournal


class StudentFormAdmin(ModelForm):
    def clean_student_group(self):
        """ Check if student is leader in any group
        If yes, then ensure it's the same as selected group. """
        # get group where current student is a leader
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(u'Студент є старостою іншої групи', code='invalid')
        return self.cleaned_data['student_group']


class StudentAdmin(admin.ModelAdmin):
    form = StudentFormAdmin
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name']
    # list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'ticket', 'notes']

    def view_on_site(self, obj):
        return reverse('students_edit', kwargs={'pk': obj.id})


class GroupFormAdmin(ModelForm):
    def clean_leader(self):
        """ Check if (student not in this group) and (student is not None)
        If yes, then ensure it's the same as selected group. """
        # get students in current group
        students = Student.objects.filter(student_group=self.instance)
        if (self.cleaned_data['leader'] not in students) and self.cleaned_data['leader']:
            raise ValidationError(u'Студент не належить цій групі', code='invalid')
        return self.cleaned_data['leader']


class GroupAdmin(admin.ModelAdmin):
    form = GroupFormAdmin
    list_display = ['title', 'leader']
    list_display_links = ['title']
    # list_editable = ['leader']
    ordering = ['title']
    list_filter = ['leader']
    list_per_page = 5
    search_fields = ['title', 'leader', 'notes']

    def view_on_site(self, obj):
        return reverse('groups_edit', kwargs={'pk': obj.id})


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(MonthJournal)


