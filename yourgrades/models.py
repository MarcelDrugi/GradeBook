from django.db import models
from django.core.validators import (RegexValidator, MaxValueValidator,
                                    MinValueValidator
                                    )
from django.contrib.auth.models import User
from .permissions import RightsSupport


class SchoolClass(models.Model):
    unique_code = models.CharField(
        unique=True,
        max_length=6,
        validators=[RegexValidator(r'^[1-8]{1}[a-z]{1}[0-9]{4}$')],
        help_text='Format: nazwa klasy(cyfra zmałą literą) łącznie z rokiem' +
                  ' zakończenia nauki - np: 1b2019'
    )
    name = models.CharField(max_length=2,
                            help_text='Cyfra i mała litera bez spacji.')
    year = models.IntegerField(
        validators=[MinValueValidator(1800), MaxValueValidator(9999)],
        help_text='Rok zakończenia nauki w formacie czterocyfrowym')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PersonalData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    first_login = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Student(PersonalData):
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    birthday = models.DateField()
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name + ' ' + self.surname


class Parent(PersonalData):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' ' + self.surname


class Teacher(PersonalData):
    email = models.EmailField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name + ' ' + self.surname


class Subject(models.Model):
    name = models.CharField(max_length=128)
    unique_code = models.CharField(
        unique=True,
        max_length=8,
        help_text='Format: dwuliterowy skrót nazwy przedmiotu z dodanym' +
                  'unikalnym kodem klasy np: Hi2c2019 (Historia w klasie 2c' +
                  'w roku szkolnym 2019)'
    )
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SubjectDate(models.Model):
    LESSONS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
        (11, '11'),
    )
    # days of the week (pl)
    DAYS = (
        ('Mo', 'Poniedizałek'),
        ('Tu', 'Wtorek'),
        ('We', 'Środa'),
        ('Th', 'Czwartek'),
        ('Fr', 'Piątek'),
        ('St', 'Sobota'),
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day = models.CharField(max_length=2, choices=DAYS)
    lesson_number = models.IntegerField(
        validators=[MaxValueValidator(12), MinValueValidator(1)],
        choices=LESSONS)


class SubjectTeachers(models.Model):
    teacher = models.ManyToManyField(Teacher)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class GradesData(models.Model):
    weight = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)])
    grade = models.IntegerField(
        validators=[MaxValueValidator(6), MinValueValidator(1)])
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Grades(GradesData):
    manager_mode = models.BooleanField(default=False)


class CanceledGrades(GradesData):
    pass


class Message(models.Model):
    text = models.TextField(max_length=1024)
    subject = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now_add=True)


class Correspondent(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Sender(Correspondent):
    message = models.OneToOneField(Message, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Recipient(Correspondent):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Mailbox(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(Sender, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class MailboxReceived(Mailbox):
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)


class MailboxSent(Mailbox):
    recipient = models.CharField(max_length=64)
