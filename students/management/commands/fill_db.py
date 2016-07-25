from random import randint
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from students.models import Student, Group
from optparse import make_option
from django.db import DatabaseError


class Command(BaseCommand):
    args = '<--student=NUM|-s NUM --group=NUM|-g NUM --user=NUM|-u NUM>'
    help = 'Creates specified number (1..10) of objects in DB.'
    option_list = BaseCommand.option_list + (
        make_option('-s', '--student', type=int, dest='student', help='Count of student objects'),
        make_option('-g', '--group', type=int, dest='group', help='Count of group objects'),
        make_option('-u', '--user', type=int, dest='user', help='Count of user objects')
    )
    models = ('student', 'group', 'user')

    def handle(self, *args, **options):
        for name in self.models:
            if options[name] and not(0 < options[name] < 11):
                raise CommandError('Number of %s objects must be in range 1..10!' % name)

        for name in self.models:
            if options[name]:
                for i in range(options[name]):
                    r1, r2, r3 = randint(1, 9999), randint(1, 9999), randint(1, 9999)
                    if name == 'student':
                        student = Student(
                            first_name='Name-{r1:04}-{r2:04}-{r3:04}'.format(r1=r1, r2=r2, r3=r3),
                            last_name='Surname-{r1:04}-{r2:04}-{r3:04}'.format(r1=r1, r2=r2, r3=r3),
                            ticket=i+1,
                            birthday=timezone.now())
                        student.save()
                    if name == 'group':
                        group = Group(
                            title='MtM-{r1:04}-{r2:04}-{r3:04}'.format(r1=r1, r2=r2, r3=r3),
                            notes='Note-{r1:04}-{r2:04}-{r3:04}'.format(r1=r1, r2=r2, r3=r3))
                        group.save()
                    if name == 'user':
                        user = User(
                            username='Username-{r1:04}-{r2:04}-{r3:04}'.format(r1=r1, r2=r2, r3=r3),
                            first_name='Name-{r1:04}-{r2:04}-{r3:04}'.format(r1=r1, r2=r2, r3=r3),
                            last_name='Surname-{r1:04}-{r2:04}-{r3:04}'.format(r1=r1, r2=r2, r3=r3),
                            email='email-{r1:04}-{r2:04}-{r3:04}@example.com'.format(r1=r1, r2=r2, r3=r3))
                        try:
                            user.save()
                        except DatabaseError:
                            self.stdout.write('Warning! User %s is not unique and do not write to DB.' % user.username)
                        else:
                            self.stdout.write('User %s created successfully.' % user.username)
