from django.contrib import admin
from .models.students import Student
from .models.groups import Group

# Register your models here.
admin.site.register(Student)
admin.site.register(Group)

