from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime
import pytz
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import *
from .forms import *


class SchoolClassTestCase(TestCase):
    def setUp(self):
        SchoolClass.objects.create(unique_code='1a2020', name='1a',
                                   year=2020)

    def test_school_class(self):
        school_class = SchoolClass.objects.get(unique_code='1a2020')
        self.assertTrue(isinstance(school_class, SchoolClass))
        self.assertEqual(school_class.unique_code[0:2], school_class.name)
        self.assertEqual(school_class.unique_code[2:6], str(school_class.year))
        self.assertEqual(len(school_class.unique_code), 6)


class StudentTestCase(TestCase):
    def setUp(self):
        user_data = {'username': 'AdamNowak', 'password': 'adamspass'}
        user = User.objects.create_user(**user_data)
        school_class_data = {'unique_code': '1b2020', 'name': '1b',
                             'year': 2020}
        school_class = SchoolClass.objects.create(**school_class_data)
        Student.objects.create(user=user, school_class=school_class,
                               name='Adam', surname='Nowak',
                               birthday='2011-03-29',
                               email='jankowalski@example.pl')

    def test_student(self):
        student = Student.objects.get(user__username='AdamNowak')
        self.assertTrue(isinstance(student, Student))
        self.assertEqual(student.first_login, True)
        self.assertEqual(student.__str__(),
                         student.name + ' ' + student.surname)
        unique_code = student.school_class.unique_code
        school_class = SchoolClass.objects.get(unique_code=unique_code)
        self.assertEqual(student.school_class, school_class)


class ParentTestCase(TestCase):
    def setUp(self):
        student_user_data = {'username': 'JanNowak', 'password': 'janspass'}
        student_user = User.objects.create_user(**student_user_data)
        school_class_data = {'unique_code': '1c2020', 'name': '1c',
                             'year': 2020}
        SchoolClass.objects.create(**school_class_data)
        school_class = SchoolClass.objects.get(
            unique_code=school_class_data['unique_code'])
        Student.objects.create(user=student_user, school_class=school_class,
                               name='Adam', surname='Nowak',
                               birthday='2011-03-29',
                               email='jankowalski@example.pl')
        student = Student.objects.get(user=student_user)
        parent_user_data = {'username': 'AnnaNowak', 'password': 'annaspass'}
        User.objects.create_user(**parent_user_data)
        parent_user = User.objects.get(username=parent_user_data['username'])
        Parent.objects.create(user=parent_user, student=student, name='Anna',
                              surname='Nowak')

    def test_parent(self):
        parent = Parent.objects.get(user__username='AnnaNowak')
        self.assertTrue(isinstance(parent, Parent))
        self.assertEqual(parent.first_login, True)
        self.assertEqual(parent.__str__(), parent.name + ' ' + parent.surname)


class TeacherTestCase(TestCase):
    def setUp(self):
        teacher_user_data = {'username': 'KarolNowak', 'password': 'karospass'}
        teacher_user = User.objects.create_user(**teacher_user_data)
        Teacher.objects.create(user=teacher_user, name='Karol',
                               surname='Nowak', email='karolnowak@example.pl')

    def test_teacher(self):
        teacher = Teacher.objects.get(user__username='KarolNowak')
        self.assertTrue(isinstance(teacher, Teacher))
        self.assertEqual(teacher.first_login, True)
        self.assertEqual(teacher.active, True)
        self.assertEqual(teacher.__str__(),
                         teacher.name + ' ' + teacher.surname)


class SubjectTestCase(TestCase):
    def setUp(self):
        school_class = SchoolClass.objects.create(unique_code='1d2020',
                                                  name='1d', year=2020)
        Subject.objects.create(name='History', unique_code='Hi1d2020',
                               school_class=school_class)

    def subject_test(self):
        subject = Subject.object.get(name='History')
        self.assertTrue(isinstance(subject, Subject))
        self.assertEqual(len(subject.unique_code), 8)
        self.assertEqual(subject.__str__(), subject.name)


class SubjectTeacherTestCase(TestCase):
    def setUp(self):
        school_class = SchoolClass.objects.create(unique_code='1e2020',
                                                  name='1e', year=2020)
        subject = Subject.objects.create(name='Chemistry',
                                         unique_code='Ch1e2020',
                                         school_class=school_class)
        teacher_user_data = {'username': 'MarcinNowak',
                             'password': 'marcinspass'}
        teacher_user = User.objects.create_user(**teacher_user_data)
        teacher = Teacher.objects.create(user=teacher_user, name='Marcin',
                                         surname='Nowak',
                                         email='marcinnowak@example.pl')
        subject_teacher = SubjectTeachers.objects.create(subject=subject)
        subject_teacher.teacher.add(teacher)

    def test_subject_teachers(self):
        subject_teachers = SubjectTeachers.objects.get(
            subject__unique_code='Ch1e2020')
        self.assertTrue(isinstance(subject_teachers, SubjectTeachers))
        self.assertEqual(subject_teachers.subject.name, 'Chemistry')


class SubjectDateTestCase(TestCase):
    def setUp(self):
        school_class = SchoolClass.objects.create(unique_code='4e2020',
                                                  name='4e', year=2020)
        subject = Subject.objects.create(name='Biology',
                                         unique_code='Bi4e2020',
                                         school_class=school_class)
        SubjectDate.objects.create(day='Mo', lesson_number=4, subject=subject)

    def test_subject_date(self):
        subject_date = SubjectDate.objects.get(subject__unique_code='Bi4e2020')
        self.assertTrue(isinstance(subject_date, SubjectDate))
        self.assertTrue(subject_date.lesson_number <= 13)
        self.assertTrue(subject_date.lesson_number >= 1)
        self.assertIn(subject_date.day, {'Mo', 'Tu', 'We', 'Th', 'Fr', 'St'})


class GradesTestCase(TestCase):
    def setUp(self):
        user_data = {'username': 'MarekNowak', 'password': 'marekspass'}
        user = User.objects.create_user(**user_data)
        school_class_data = {'unique_code': '1f2020', 'name': '1f',
                             'year': 2020}
        school_class = SchoolClass.objects.create(**school_class_data)
        student = Student.objects.create(user=user, school_class=school_class,
                                         name='Marek', surname='Nowak',
                                         birthday='2011-04-11',
                                         email='mareknowak@example.pl')
        subject = Subject.objects.create(name='Maths', unique_code='Ma1d2020',
                                         school_class=school_class)
        Grades.objects.create(weight=8, grade=5, student=student,
                              subject=subject)

    def test_grades(self):
        grade = Grades.objects.get(student__user__username='MarekNowak')
        self.assertTrue(isinstance(grade, Grades))
        now = pytz.utc.localize(datetime.now())
        self.assertTrue(grade.date <= now)
        self.assertTrue(1 <= grade.weight <= 10)
        self.assertTrue(1 <= grade.grade <= 6)


class CanceledGradesTestCase(TestCase):
    def setUp(self):
        user_data = {'username': 'KamilNowak', 'password': 'kamilspass'}
        user = User.objects.create_user(**user_data)
        school_class_data = {'unique_code': '1g2020', 'name': '1g',
                             'year': 2020}
        school_class = SchoolClass.objects.create(**school_class_data)
        student = Student.objects.create(user=user, school_class=school_class,
                                         name='Kamil', surname='Nowak',
                                         birthday='2010-04-11',
                                         email='kamilnowak@example.pl')
        subject = Subject.objects.create(name='Gym', unique_code='Gy1d2020',
                                         school_class=school_class)
        CanceledGrades.objects.create(weight=9, grade=4, student=student,
                                      subject=subject)

    def test_grades(self):
        canceled_grade = CanceledGrades.objects.get(
            student__user__username='KamilNowak')
        self.assertTrue(isinstance(canceled_grade, CanceledGrades))
        now = pytz.utc.localize(datetime.now())
        self.assertTrue(canceled_grade.date <= now)
        self.assertTrue(1 <= canceled_grade.weight <= 10)
        self.assertTrue(1 <= canceled_grade.grade <= 6)


class MessageTestCase(TestCase):
    def setUp(self):
        Message.objects.create(id=1, subject='Test subject', text='Test text.')

    def test_message(self):
        message = Message.objects.get(id=1)
        self.assertTrue(isinstance(message, Message))
        now = pytz.utc.localize(datetime.now())
        self.assertTrue(message.date <= now)
        max_length = message._meta.get_field('text').max_length
        self.assertEqual(max_length, 1024)
        self.assertTrue(len(message.text) <= 1024)
        self.assertTrue(len(message.subject) <= 128)


class SenderTestCse(TestCase):
    def setUp(self):
        message = Message.objects.create(id=2, subject='Test subject',
                                         text='Test text.')
        user_data = {'username': 'JanMalinowski', 'password': 'janspass'}
        user = User.objects.create_user(**user_data)
        user.first_name = 'Jan'
        user.last_name = 'Malinowski'
        user.save()
        Sender.objects.create(user=user, message=message)

    def test_sender(self):
        sender = Sender.objects.get(message__id=2)
        self.assertTrue(isinstance(sender, Sender))
        self.assertEqual(sender.__str__(),
                         sender.user.first_name + ' ' + sender.user.last_name)


class RecipientTestCase(TestCase):
    def setUp(self):
        message = Message.objects.create(id=3, subject='Test subject',
                                         text='Test text.')
        user_data = {'username': 'AdamMalinowski', 'password': 'adamspass'}
        user = User.objects.create_user(**user_data)
        user.save()
        Recipient.objects.create(user=user, message=message)

    def test_recipient(self):
        recipient = Recipient.objects.get(message__id=3)
        self.assertTrue(isinstance(recipient, Recipient))
        self.assertEqual(recipient.message.subject, 'Test subject')


class MailboxReceivedTestCase(TestCase):
    def setUp(self):
        message = Message.objects.create(id=4, subject='Test subject',
                                         text='Test text.')
        user_recipient_data = {'username': 'AdamRak', 'password': 'adamspass'}
        user_recipient = User.objects.create_user(**user_recipient_data)
        recipient = Recipient.objects.create(user=user_recipient,
                                             message=message)
        user_sender_data = {'username': 'AdamRyba', 'password': 'adamspass'}
        user_sender = User.objects.create_user(**user_sender_data)
        sender = Sender.objects.create(user=user_sender, message=message)
        MailboxReceived.objects.create(sender=sender, recipient=recipient,
                                       message=message)

    def test_mailbox_received(self):
        mailbox_received = MailboxReceived.objects.get(message__id=4)
        sender = Sender.objects.get(user__username='AdamRyba')
        recipient = Recipient.objects.get(user__username='AdamRak')
        self.assertTrue(isinstance(mailbox_received, MailboxReceived))
        self.assertEqual(mailbox_received.read, False)
        self.assertEqual(sender.message, recipient.message)


class MailboxSentTestCase(TestCase):
    def setUp(self):
        message = Message.objects.create(id=5, subject='Test subject',
                                         text='Test text.')
        recipient = 'Mr Jan Rak'
        user_sender_data = {'username': 'JanRyba', 'password': 'adamspass'}
        user_sender = User.objects.create_user(**user_sender_data)
        sender = Sender.objects.create(user=user_sender, message=message)
        MailboxSent.objects.create(sender=sender, recipient=recipient,
                                       message=message)

    def test_mailbox_received(self):
        mailbox_sent = MailboxSent.objects.get(message__id=5)
        self.assertTrue(isinstance(mailbox_sent, MailboxSent))
        max_length = mailbox_sent._meta.get_field('recipient').max_length
        self.assertEqual(max_length, 64)

'''
Views tests   |________________________________________________________________
'''


def create_user(password):
    username = 'tester'
    numbering = 0
    while True:
        try:
            User.objects.get(username=username)
            numbering += 1
            username += str(numbering)
        except User.DoesNotExist:
            return User.objects.create_user(
                username=username, password=password,
                first_name='Name', last_name='Surname')


def create_person(kind, password):
    content_type = ContentType.objects.get_for_model(RightsSupport)
    permission = Permission.objects.get(content_type=content_type,
                                        codename=kind)
    if kind in {'student', 'parent'}:
        user = create_user(password)
        user.user_permissions.add(permission)
        try:
            school_class = SchoolClass.objects.get(unique_code='2a2020')
        except SchoolClass.DoesNotExist:
            school_class = SchoolClass.objects.create(unique_code='2a2020',
                                                      name='2a', year=2020)
        student = Student.objects.create(user=user,
                                         school_class=school_class,
                                         name=user.first_name,
                                         surname=user.last_name,
                                         birthday='2010-03-29')
        if kind == 'student':
            return student
        if kind == 'parent':
            user = create_user(password)
            user.user_permissions.add(permission)
            return Parent.objects.create(user=user, student=student,
                                         name=user.first_name,
                                         surname=user.last_name)
    if kind == 'teacher':
        user = create_user(password)
        user.user_permissions.add(permission)
        return Teacher.objects.create(user=user, name=user.first_name,
                                      surname=user.last_name)


def create_manager(password):
    username = 'tester'
    numbering = 0
    while True:
        try:
            User.objects.get(username=username)
            numbering += 1
            username += str(numbering)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            first_name='Name',
                                            last_name='Surname')
            content_type = ContentType.objects.get_for_model(RightsSupport)
            permission = Permission.objects.get(content_type=content_type,
                                                codename='manager')
            user.user_permissions.add(permission)
            return user


class HomepageViewTestCase(TestCase):
    def setUp(self):
        password = 'testerspass'
        # Create users and student/parent/teacher models objects to test login
        # by homepage
        self.student_1 = create_person('student', password)
        self.student_1_form_data = {'username': self.student_1.user.username,
                                    'password': password}
        self.student_2 = create_person('student', password)
        self.student_2.first_login = False
        self.student_2.save()
        self.student_2_form_data = {'username': self.student_2.user.username,
                                    'password': password}

        self.parent_1 = create_person('parent', password)
        self.parent_1_form_data = {'username': self.parent_1.user.username,
                                    'password': password}
        self.parent_2 = create_person('parent', password)
        self.parent_2.first_login = False
        self.parent_2.save()
        self.parent_2_form_data = {'username': self.parent_2.user.username,
                                   'password': password}

        self.teacher_1 = create_person('teacher', password)
        self.teacher_1_form_data = {'username': self.teacher_1.user.username,
                                    'password': password}
        self.teacher_2 = create_person('teacher', password)
        self.teacher_2.first_login = False
        self.teacher_2.save()
        self.teacher_2_form_data = {'username': self.teacher_2.user.username,
                                    'password': password}

    def test_homepage_view(self):
        response = Client().get(reverse('yourgrades:homepage'))
        self.assertEqual(response.status_code, 200)
        # Post with clean form or with wrong data -> not redirects
        response = Client().post(reverse('yourgrades:homepage'))
        self.assertEqual(response.status_code, 200)
        response = Client().post(reverse('yourgrades:homepage'),
                                 {'username': 'tester',
                                  'password': 'wrongpass'})
        self.assertEqual(response.status_code, 200)

        # Student redirection tests
        # if first_login field is True -> redirects to FirstLoginView
        self.assertTrue(LoginForm(self.student_1_form_data).is_valid())
        response = Client().post(reverse('yourgrades:homepage'),
                                 self.student_1_form_data, )
        self.assertEqual(response.status_code, 302)
        response = Client().post(reverse('yourgrades:homepage'),
                                 self.student_1_form_data, follow=True)
        self.assertRedirects(response, '/yourgrades/firstlogin')

        # if first_login field is False, redirects to StudentParentView
        self.assertTrue(LoginForm(self.student_2_form_data).is_valid())
        response = Client().post(reverse('yourgrades:homepage'),
                                 self.student_2_form_data, )
        self.assertEqual(response.status_code, 302)
        response = Client().post(reverse('yourgrades:homepage'),
                                 self.student_2_form_data, follow=True)
        self.assertRedirects(response, '/yourgrades/studentparent')
        self.assertTemplateUsed(response, 'yourgrades/studentparent.html')

        # Parent redirection tests
        # if first_login field is True, redirects to FirstLoginView
        self.assertTrue(LoginForm(self.parent_1_form_data).is_valid())
        response = Client().post(reverse('yourgrades:homepage'),
                                 self.parent_1_form_data, )
        self.assertEqual(response.status_code, 302)
        response = Client().post(reverse('yourgrades:homepage'),
                                 self.parent_1_form_data, follow=True)
        self.assertRedirects(response, '/yourgrades/firstlogin')

        # if first_login field is False, redirects to StudentParentView
        self.assertTrue(LoginForm(self.parent_2_form_data).is_valid())
        response = Client().post(reverse('yourgrades:homepage'),
                                 self.parent_2_form_data, )
        self.assertEqual(response.status_code, 302)
        response = Client().post(reverse('yourgrades:homepage'),
                                 self.parent_2_form_data, follow=True)
        self.assertRedirects(response, '/yourgrades/studentparent')
        self.assertTemplateUsed(response, 'yourgrades/studentparent.html')

        # Teacher redirection tests
        # if first_login field is True, redirects to FirstLoginView
        self.assertTrue(LoginForm(self.teacher_1_form_data).is_valid())
        response = Client().post(reverse('yourgrades:homepage'),
                                 self.teacher_1_form_data, )
        self.assertEqual(response.status_code, 302)
        response = Client().post(reverse('yourgrades:homepage'),
                                 self.teacher_1_form_data, follow=True)
        self.assertRedirects(response, '/yourgrades/firstlogin')

        # if first_login field is False, redirects to TeacherPanelView
        self.assertTrue(LoginForm(self.teacher_2_form_data).is_valid())
        response = Client().post(reverse('yourgrades:homepage'),
                                 self.teacher_2_form_data, )
        self.assertEqual(response.status_code, 302)
        response = Client().post(reverse('yourgrades:homepage'),
                                 self.teacher_2_form_data, follow=True)
        self.assertRedirects(response, '/yourgrades/teacher')
        self.assertTemplateUsed(response, 'yourgrades/teacher.html')


class LogOutViewTestCase(TestCase):
    def setUp(self):
        password = 'testerspass'
        user = create_user(password)
        self.client = Client()
        self.client.login(username=user.username, password=password)

    def test_logout(self):
        response = self.client.get(reverse('yourgrades:logout'))
        self.assertEqual(response.status_code, 302)
        # Logout redirects to homepage
        response = self.client.get(reverse('yourgrades:logout'), follow=True)
        self.assertRedirects(response, '/yourgrades')


class FirstLoginViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        no_perm_user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=no_perm_user.username,
                            password=self.password)
        # Create Student (with assigned User) and login him
        self.student = create_person('student', self.password)
        self.client_2 = Client()
        self.client_2.login(username=self.student.user.username,
                            password=self.password)

    def test_first_login(self):
        # GET, user without permission -> 403
        response = self.client_1.get(reverse('yourgrades:first_login'))
        self.assertEqual(response.status_code, 403)
        # GET, user with permission -> 200
        response = self.client_2.get(reverse('yourgrades:first_login'))
        self.assertEqual(response.status_code, 200)
        # POST with wrong form data (or no form data) -> no redirection
        response = self.client_2.post(reverse('yourgrades:first_login'),
                                      {'username': '', 'password': 'anything',
                                       'password_confirm': 'incorrect'})
        self.assertEqual(response.status_code, 200)
        # POST, user with good permission and correct form
        # -> redirection to assigned panel
        form_data = {'username': 'newusername', 'password': 'newpass',
                     'password_confirm': 'newpass'}
        self.assertTrue(FirstLoginForm(form_data).is_valid())
        response = self.client_2.post(reverse('yourgrades:first_login'),
                                      form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/yourgrades/studentparent')
        response = self.client_2.post(reverse('yourgrades:first_login'),
                                      form_data, follow=True)
        self.assertTemplateUsed(response, 'yourgrades/studentparent.html')


class ManagerPanelViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)

    def test_manager_panel(self):
        # User without manager permission -> 403
        response = self.client_1.get(reverse('yourgrades:manager'))
        self.assertEqual(response.status_code, 403)
        # User with manager permission -> 200
        response = self.client_2.get(reverse('yourgrades:manager'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/manager.html')


class CreateSchoolClassViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)

    def test_create_school_class(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(reverse('yourgrades:create_school_class'))
        self.assertEqual(response.status_code, 403)
        # GET, user with manager permission -> 200
        response = self.client_2.get(reverse('yourgrades:create_school_class'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'yourgrades/managercreateschoolclass.html')

        # POST with wrong form data (or no form data) -> no redirection
        response = self.client_2.post(
            reverse('yourgrades:create_school_class'),
            {'name': '2b', 'year': 2020, 'unique_code': 'wrong_code'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'yourgrades/managercreateschoolclass.html')
        # POST, user with good permission and correct form
        # -> redirect to manager view
        form_data = {'name': '2b', 'year': 2020, 'unique_code': '2b2020'}
        self.assertTrue(SchoolClassForm(form_data).is_valid())
        response = self.client_2.post(
            reverse('yourgrades:create_school_class'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/yourgrades/manager')
        response = self.client_2.post(
            reverse('yourgrades:create_school_class'), form_data, follow=True)
        self.assertTemplateUsed(response,
                                'yourgrades/managercreateschoolclass.html')
        # Check school class creation
        self.assertTrue(SchoolClass.objects.filter(unique_code='2b2020'))


class EditSchoolClassViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)
        SchoolClass.objects.create(name='2c', year=2020, unique_code='2c2020')

    def test_edit_school_class(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:edit_school_class',
                kwargs={'class_unique_code': '2c2020'}
            )
        )
        self.assertEqual(response.status_code, 403)
        # GET, user with manager permission -> 200
        response = self.client_2.get(
            reverse(
                'yourgrades:edit_school_class',
                kwargs={'class_unique_code': '2c2020'}
            )
        )
        self.assertEqual(response.status_code, 200)
        # POST with wrong form data (or no form data) -> no redirection
        response = self.client_2.post(
            reverse(
                'yourgrades:edit_school_class',
                kwargs={'class_unique_code': '2c2020'}
            ),
            {
                'name': 'Jan',
                'surname': '',
                'birthday': '2011-10-14',
                'first_parent_name': 'Adam',
                'first_parent_surname': 'Kowalski'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'yourgrades/managereditschoolclass.html')
        # POST, user with good permission and correct form
        # -> redirect view to itself
        form_data = {'name': 'Jan', 'surname': 'Kowalski',
                     'birthday': '2011-10-14', 'first_parent_name': 'Adam',
                     'first_parent_surname': 'Kowalski'}
        self.assertTrue(CreateStudentForm(form_data).is_valid())
        response = self.client_2.post(
            reverse(
                'yourgrades:edit_school_class',
                kwargs={'class_unique_code': '2c2020'}
            ),
            form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             '/yourgrades/manager/editschoolclass/2c2020')
        response = self.client_2.post(
            reverse(
                'yourgrades:edit_school_class',
                kwargs={'class_unique_code': '2c2020'}
            ),
            form_data,
            follow=True
        )
        self.assertTemplateUsed(response,
                                'yourgrades/managereditschoolclass.html')
        # Check student and parent creation
        self.assertTrue(Student.objects.filter(name='Jan', surname='Kowalski'))
        self.assertTrue(Parent.objects.filter(name='Adam', surname='Kowalski'))


class DeactivationSchoolClassViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)
        SchoolClass.objects.create(name='2d', year=2020, unique_code='2d2020')

    def test_deactivation_school_class(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse('yourgrades:deactivation_school_class',
                    kwargs={'class_unique_code': '2d2020'}))
        self.assertEqual(response.status_code, 403)
        # GET, user with permission -> 405
        response = self.client_2.get(
            reverse('yourgrades:deactivation_school_class',
                    kwargs={'class_unique_code': '2d2020'}))
        self.assertEqual(response.status_code, 405)
        # POST, user with good permission redirect to edit_school_class view
        response = self.client_2.post(
            reverse('yourgrades:deactivation_school_class',
                    kwargs={'class_unique_code': '2d2020'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             '/yourgrades/manager/editschoolclass/2d2020')
        # Check class deactivation
        school_class = SchoolClass.objects.get(unique_code='2d2020')
        self.assertEqual(school_class.active, False)


class DeactivationTeacherViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)
        self.teacher = create_person('teacher', self.password)

    def test_deactivation_teacher(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:deactivation_teacher',
                kwargs={'teacher_user_id': self.teacher.user.id}
            )
        )
        self.assertEqual(response.status_code, 403)
        # GET, user with good permission redirect to manager panel view
        response = self.client_2.get(
            reverse(
                'yourgrades:deactivation_teacher',
                kwargs={'teacher_user_id': self.teacher.user.id}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/yourgrades/manager')
        # Check class deactivation
        teacher = Teacher.objects.get(user__id=self.teacher.user.id)
        self.assertEqual(teacher.active, False)


class ActivationSchoolClassViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)
        SchoolClass.objects.create(name='2e', year=2020, unique_code='2e2020',
                                   active=False)

    def test_activation_school_class(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse('yourgrades:activation_school_class',
                    kwargs={'class_unique_code': '2e2020'}))
        self.assertEqual(response.status_code, 403)
        # GET, user with permission -> 405
        response = self.client_2.get(
            reverse('yourgrades:activation_school_class',
                    kwargs={'class_unique_code': '2e2020'}))
        self.assertEqual(response.status_code, 405)
        # POST, user with good permission redirect to edit_school_class view
        response = self.client_2.post(
            reverse('yourgrades:activation_school_class',
                    kwargs={'class_unique_code': '2e2020'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             '/yourgrades/manager/editschoolclass/2e2020')
        # Check class activation
        school_class = SchoolClass.objects.get(unique_code='2e2020')
        self.assertEqual(school_class.active, True)


class DeleteStudentViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)
        self.parent = create_person('parent', self.password)

    def test_delete_student(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(reverse('yourgrades:del_student', kwargs={
            'user_id': self.parent.student.user.id}))
        self.assertEqual(response.status_code, 403)
        # GET, user with manager permission
        # -> redirect to edit_school_class view
        response = self.client_2.get(reverse('yourgrades:del_student', kwargs={
            'user_id': self.parent.student.user.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '/yourgrades/manager/editschoolclass/' +
            self.parent.student.school_class.unique_code
        )
        # Check student deletion
        self.assertFalse(
            Student.objects.filter(user__id=self.parent.student.user.id))


class AddTeacherViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)

    def test_add_teacher(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(reverse('yourgrades:add_teacher'))
        self.assertEqual(response.status_code, 403)
        # GET, user with manager permission -> 200
        response = self.client_2.get(reverse('yourgrades:add_teacher'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/manageraddteacher.html')

        # POST with wrong form data (or no form data) -> no redirection
        response = self.client_2.post(
            reverse('yourgrades:add_teacher'), {'name': '', 'surname': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/manageraddteacher.html')
        # POST, user with good permission and correct form
        # -> redirect to manager view
        form_data = {'name': 'Anna', 'surname': 'Malinowska'}
        self.assertTrue(CreateTeacherForm(form_data).is_valid())
        response = self.client_2.post(
            reverse('yourgrades:add_teacher'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/yourgrades/manager')
        response = self.client_2.post(
            reverse('yourgrades:add_teacher'), form_data, follow=True)
        self.assertTemplateUsed(response, 'yourgrades/manager.html')


class AddSubjectViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)
        self.school_class = SchoolClass.objects.create(name='3a', year=2020,
                                                       unique_code='3a2020')
        self.teacher = create_person('teacher', self.password)

    def test_add_teacher(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(reverse('yourgrades:add_subject', kwargs={
            'class_unique_code': self.school_class.unique_code}))
        self.assertEqual(response.status_code, 403)
        # GET, user with manager permission -> 200
        response = self.client_2.get(reverse('yourgrades:add_subject', kwargs={
            'class_unique_code': self.school_class.unique_code}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/manageraddsubject.html')

        # POST with wrong form data (or no form data) -> no redirection
        response = self.client_2.post(
            reverse(
                'yourgrades:add_subject',
                kwargs={'class_unique_code': self.school_class.unique_code}
            ),
            {'name': 'Physics', 'shortcut': '', 'teachers': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/manageraddsubject.html')
        # POST, user with good permission and correct form
        # -> redirect to edit_school_class view
        form_data = {'name': 'Physics', 'shortcut': 'Ph',}
        self.assertTrue(CreateSubjectForm(form_data).is_valid())
        response = self.client_2.post(
            reverse(
                'yourgrades:add_subject',
                kwargs={'class_unique_code': self.school_class.unique_code}
            ),
            form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/yourgrades/manager/editschoolclass/' +
                             self.school_class.unique_code)
        # Check Subject and Subject_teacher objects creation
        self.assertTrue(Subject.objects.filter(name='Physics'))
        subject = Subject.objects.get(name='Physics')
        self.assertEqual(subject.unique_code,
                         form_data['shortcut'] + self.school_class.unique_code)


class ManagerSubjectViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)
        self.school_class = SchoolClass.objects.create(name='3b', year=2020,
                                                       unique_code='3b2020')
        self.subject = Subject.objects.create(name='History',
                                              unique_code='Hi3b2020',
                                              school_class=self.school_class)

    def test_manager_subject(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:subject_view',
                kwargs={
                    'class_unique_code': self.school_class.unique_code,
                    'subject_unique_code': self.subject.unique_code
                }
            )
        )
        self.assertEqual(response.status_code, 403)
        # GET, user with manager permission -> 200
        response = self.client_2.get(
            reverse(
                'yourgrades:subject_view',
                kwargs={
                    'class_unique_code': self.school_class.unique_code,
                    'subject_unique_code': self.subject.unique_code
                }
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'yourgrades/managersubjectpanel.html')
        # Check created context:
        self.assertEqual(response.context['subject'], self.subject)
        self.assertEqual(response.context['class'], self.school_class)
        # POST, user with manager permission and correct form
        # -> redirection view to itself
        form_data = {'day': 'Mo', 'lesson_number': 3}
        self.assertTrue(AddSubjectDateForm(form_data).is_valid())
        response = self.client_2.post(
            reverse(
                'yourgrades:subject_view',
                kwargs={
                    'class_unique_code': self.school_class.unique_code,
                    'subject_unique_code': self.subject.unique_code
                }
            ),
            form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '/yourgrades/manager/editschoolclass/' +
            self.school_class.unique_code + '/' + self.subject.unique_code
        )


class DeleteSubjectDateViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)
        self.school_class = SchoolClass.objects.create(name='5b', year=2020,
                                                       unique_code='5b2020')
        self.subject = Subject.objects.create(name='Gym',
                                              unique_code='Gy5b2020',
                                              school_class=self.school_class)
        self.date = SubjectDate.objects.create(subject=self.subject, day='Fr',
                                               lesson_number=5)

    def test_delete_subject_date(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:delete_date',
                kwargs={
                    'class_unique_code': self.school_class.unique_code,
                    'subject_unique_code': self.subject.unique_code,
                    'day': 5,
                    'lesson': self.date.lesson_number
                }
            )
        )
        self.assertEqual(response.status_code, 403)
        # GET, user with manager permission -> redirection subject_view
        response = self.client_2.get(
            reverse(
                'yourgrades:delete_date',
                kwargs={
                    'class_unique_code': self.school_class.unique_code,
                    'subject_unique_code': self.subject.unique_code,
                    'day': 5,
                    'lesson': self.date.lesson_number
                }
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '/yourgrades/manager/editschoolclass/' +
            self.school_class.unique_code + '/' + self.subject.unique_code
        )


class TimetableViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        self.teacher = create_person('teacher', self.password)
        self.client_2 = Client()
        self.client_2.login(username=self.teacher.user.username,
                            password=self.password)
        self.student = create_person('student', self.password)
        self.client_3 = Client()
        self.client_3.login(username=self.student.user.username,
                            password=self.password)

    def test_timetable(self):
        # GET, user without student/parent/teacher  permission -> 403
        response = self.client_1.get(
            reverse('yourgrades:timetable', kwargs={'person': 'student'}))
        self.assertEqual(response.status_code, 403)

        # GET, user with student/parent permission -> 200
        response = self.client_2.get(
            reverse('yourgrades:timetable', kwargs={'person': 'teacher'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/timetable.html')
        # Checking returned context
        self.assertEqual(response.context['person'], 'teacher')

        # GET, user with teacher permission -> 200
        response = self.client_3.get(
            reverse('yourgrades:timetable', kwargs={'person': 'student'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/timetable.html')
        # Checking returned context
        self.assertEqual(response.context['person'], 'student')


class ManagerStudentViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)
        self.parent = create_person('parent', self.password)
        self.subject = Subject.objects.create(
            name='Maths',
            unique_code='Ma' + self.parent.student.school_class.unique_code,
            school_class=self.parent.student.school_class
        )

    def test_manager_student(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:manager_student',
                kwargs={'user_id': self.parent.student.user.id}
            )
        )
        self.assertEqual(response.status_code, 403)
        # GET, user with manager permission -> 200
        response = self.client_2.get(
            reverse(
                'yourgrades:manager_student',
                kwargs={'user_id': self.parent.student.user.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/managerstudent.html')
        # POST with wrong form data (or no form data) -> no redirection
        response = self.client_2.post(
            reverse(
                'yourgrades:manager_student',
                kwargs={'user_id': self.parent.student.user.id}
            ),
            {'grade': '', 'weight': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/managerstudent.html')
        # POST, user with good permission and correct form
        # -> redirect view to itself
        response = self.client_2.post(
            reverse(
                'yourgrades:manager_student',
                kwargs={'user_id': self.parent.student.user.id}
            ),
            {'grade': 5, 'weight': 8, 'subject': self.subject.unique_code}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/yourgrades/manager/student/' + str(
            self.parent.student.user.id))
        # Checking Grades model object
        self.assertTrue(Grades.objects.filter(subject=self.subject,
                                              student=self.parent.student))


class ManagerGradesHistoryViewTestCasee(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)

    def test_delete_student(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(reverse('yourgrades:manager_history'))
        self.assertEqual(response.status_code, 403)
        # GET, user with manager permission -> 200
        response = self.client_2.get(reverse('yourgrades:manager_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/managerhistory.html')


class DeleteSubjectViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)
        self.school_class = SchoolClass.objects.create(name='4a', year=2020,
                                                       unique_code='4a2020')
        self.subject = Subject.objects.create(name='Gym',
                                              unique_code='Gy4a2020',
                                              school_class=self.school_class)

    def test_delete_student(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:del_subject',
                kwargs={
                    'class_unique_code': self.school_class.unique_code,
                    'subject_unique_code': self.subject.unique_code
                }
            )
        )
        self.assertEqual(response.status_code, 403)
        # GET, user with manager permission
        # -> redirect to edit_school_class view
        response = self.client_2.get(
            reverse(
                'yourgrades:del_subject',
                kwargs={
                    'class_unique_code': self.school_class.unique_code,
                    'subject_unique_code': self.subject.unique_code
                }
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/yourgrades/manager/editschoolclass/' +
                             str(self.school_class.unique_code))


class DeleteSubjectTeacherViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)
        self.school_class = SchoolClass.objects.create(name='4a', year=2020,
                                                       unique_code='4a2020')
        self.subject = Subject.objects.create(name='Gym',
                                              unique_code='Gy4a2020',
                                              school_class=self.school_class)
        self.teacher = create_person('teacher', self.password)
        subject_teachers = SubjectTeachers.objects.create(subject=self.subject)
        subject_teachers.teacher.add(self.teacher)

    def test_delete_subject_teacher(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:del_subject_teacher',
                kwargs={
                    'class_unique_code': self.school_class.unique_code,
                    'subject_unique_code': self.subject.unique_code,
                    'teacher_user_id': self.teacher.user.id
                }
            ),
            HTTP_REFERER=reverse(
                'yourgrades:edit_school_class',
                kwargs={
                    'class_unique_code': self.school_class.unique_code
                }
            )
        )
        self.assertEqual(response.status_code, 403)
        # GET, user with manager permission
        # -> redirect to edit_school_class view
        response = self.client_2.get(
            reverse(
                'yourgrades:del_subject_teacher',
                kwargs={
                    'class_unique_code': self.school_class.unique_code,
                    'subject_unique_code': self.subject.unique_code,
                    'teacher_user_id': self.teacher.user.id
                }
            ),
            HTTP_REFERER=reverse(
                'yourgrades:edit_school_class',
                kwargs={
                    'class_unique_code': self.school_class.unique_code
                }
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/yourgrades/manager/editschoolclass/' +
                             str(self.school_class.unique_code))


class ManagerDeleteTeacherViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)
        self.teacher_1 = create_person('teacher', self.password)
        self.teacher_2 = create_person('teacher', self.password)

    def test_manager_delete_teacher(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:manager_del_teacher',
                kwargs={'teacher_user_id': self.teacher_1.user.id}
            )
        )
        self.assertEqual(response.status_code, 403)
        # GET, user with manager permission -> redirect to manager view
        response = self.client_2.get(
            reverse(
                'yourgrades:manager_del_teacher',
                kwargs={'teacher_user_id': self.teacher_1.user.id}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/yourgrades/manager')
        response = self.client_2.get(
            reverse(
                'yourgrades:manager_del_teacher',
                kwargs={'teacher_user_id': self.teacher_2.user.id}
            ),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/manager.html')


class ManagerResetUserViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)
        self.student = create_person('student', self.password)

    def test_reset_user(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:manager_reset_user',
                kwargs={'user_id': self.student.user.id, 'prefix': 123}
            ),
            HTTP_REFERER=reverse(
                'yourgrades:edit_school_class',
                kwargs={
                    'class_unique_code': self.student.school_class.unique_code
                }
            )
        )
        self.assertEqual(response.status_code, 403)
        # GET, user with manager permission -> redirect to manager view
        response = self.client_2.get(
            reverse(
                'yourgrades:manager_reset_user',
                kwargs={'user_id': self.student.user.id, 'prefix': 123}
            ),
            HTTP_REFERER=reverse(
                'yourgrades:edit_school_class',
                kwargs={
                    'class_unique_code': self.student.school_class.unique_code
                }
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/yourgrades/manager/editschoolclass/' +
                             str(self.student.school_class.unique_code))
        response = self.client_2.get(
            reverse(
                'yourgrades:manager_reset_user',
                kwargs={'user_id': self.student.user.id, 'prefix': 123}
            ),
            HTTP_REFERER=reverse(
                'yourgrades:edit_school_class',
                kwargs={
                    'class_unique_code': self.student.school_class.unique_code
                }
            ),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'yourgrades/managereditschoolclass.html')


class ManagerTeacherEditViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)
        self.teacher = create_person('teacher', self.password)

    def test_manager_teacher_edit(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:manager_teacher_edit',
                kwargs={'user_id': self.teacher.user.id}
            )
        )
        self.assertEqual(response.status_code, 403)
        # GET, user with manager permission -> 200
        response = self.client_2.get(
            reverse(
                'yourgrades:manager_teacher_edit',
                kwargs={'user_id': self.teacher.user.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/managereditteacher.html')

        # POST with wrong form data (or no form data) -> no redirection
        response = self.client_2.post(
            reverse(
                'yourgrades:manager_teacher_edit',
                kwargs={'user_id': self.teacher.user.id}
            ),
            {'name': '', 'surname': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/managereditteacher.html')
        # POST, user with good permission and correct form
        # -> redirect to manager view
        form_data = {'name': 'Somename', 'surname': 'Somesurname'}
        self.assertTrue(CreateTeacherForm(form_data).is_valid())
        response = self.client_2.post(
            reverse(
                'yourgrades:manager_teacher_edit',
                kwargs={'user_id': self.teacher.user.id}
            ),
            form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/yourgrades/manager/teacher/' + str(
            self.teacher.user.id))
        response = self.client_2.post(
            reverse(
                'yourgrades:manager_teacher_edit',
                kwargs={'user_id': self.teacher.user.id}
            ), follow=True
        )
        self.assertTemplateUsed(response, 'yourgrades/managereditteacher.html')
        # Checking Teacher objects change
        self.assertTrue(
            Teacher.objects.filter(name='Somename', surname='Somesurname'))


class ManagerStudentEditViewTestCse(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)
        self.parent = create_person('parent', self.password)

    def test_manager_student_edit(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:manager_student_edit',
                kwargs={'user_id': self.parent.student.user.id}
            )
        )
        self.assertEqual(response.status_code, 403)
        # GET, user with manager permission -> 200
        response = self.client_2.get(
            reverse(
                'yourgrades:manager_student_edit',
                kwargs={'user_id': self.parent.student.user.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/managereditstudent.html')
        # POST, user with good permission and correct form
        # -> redirect to manager_student view
        form_data = {'name': 'Somename', 'surname': 'Somesurname',
                     'birthday': '2010-02-24',
                     'first_parent_name': 'Othername',
                     'first_parent_surname': 'Othersurname'}
        self.assertTrue(CreateStudentForm(form_data).is_valid())
        response = self.client_2.post(
            reverse(
                'yourgrades:manager_student_edit',
                kwargs={'user_id': self.parent.student.user.id}
            ),
            form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/yourgrades/manager/student/' + str(
            self.parent.student.user.id))


class AddSubjectTeacherViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)
        self.school_class = SchoolClass.objects.create(name='4a', year=2020,
                                                       unique_code='4a2020')
        self.subject = Subject.objects.create(name='History',
                                              unique_code='Hi4a2020',
                                              school_class=self.school_class)
        self.teacher = create_person('teacher', self.password)

    def test_add_subject_teacher(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:add_subject_teacher',
                kwargs={
                    'class_unique_code': self.school_class.unique_code,
                    'subject_unique_code': self.subject.unique_code,
                }
            )
        )
        self.assertEqual(response.status_code, 403)
        # GET, user with manager permission -> 200
        response = self.client_2.get(
            reverse(
                'yourgrades:add_subject_teacher',
                kwargs={
                    'class_unique_code': self.school_class.unique_code,
                    'subject_unique_code': self.subject.unique_code,
                }
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'yourgrades/manageraddsubjectteacher.html')


class ManagerTeacherViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        user_manager = create_manager(self.password)
        self.client_2 = Client()
        self.client_2.login(username=user_manager.username,
                            password=self.password)
        self.teacher = create_person('teacher', self.password)

    def test_manager_teacher(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:manager_teacher',
                kwargs={'teacher_user_id': self.teacher.user.id}
            )
        )
        self.assertEqual(response.status_code, 403)
        # GET, user with manager permission -> 200
        response = self.client_2.get(
            reverse(
                'yourgrades:manager_teacher',
                kwargs={'teacher_user_id': self.teacher.user.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/managerteacher.html')


class TeacherPanelViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        teacher_1 = create_person('teacher', self.password)
        teacher_1.first_login = False
        teacher_1.save()
        self.client_2 = Client()
        self.client_2.login(username=teacher_1.user.username,
                            password=self.password)

        teacher_2 = create_person('teacher', self.password)
        self.client_3 = Client()
        self.client_3.login(username=teacher_2.user.username,
                            password=self.password)

    def test_teacher_panel(self):
        # GET,user without teacher permission -> 403
        response = self.client_1.get(reverse('yourgrades:teacher'))
        self.assertEqual(response.status_code, 403)
        # GET, user with teacher permission and first_login = False -> 200
        response = self.client_2.get(reverse('yourgrades:teacher'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/teacher.html')
        # GET, user with teacher permission and first_login = True
        # -> redirect to first_login view
        response = self.client_3.get(reverse('yourgrades:teacher'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/yourgrades/firstlogin')


class TeacherSubjectViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)

        self.teacher = create_person('teacher', self.password)
        self.client_2 = Client()
        self.client_2.login(username=self.teacher.user.username,
                            password=self.password)
        self.student = create_person('student', self.password)
        self.subject = Subject.objects.create(
            name='English',
            unique_code='En4d2020',
            school_class=self.student.school_class
        )

    def test_teacher_subject(self):
        # GET, user without teacher permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:teacher_subject',
                kwargs={'subject_unique_code': self.subject.unique_code}
            )
        )
        self.assertEqual(response.status_code, 403)
        # GET, user with teacher permission -> 200
        response = self.client_2.get(
            reverse(
                'yourgrades:teacher_subject',
                kwargs={'subject_unique_code': self.subject.unique_code}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/teachersubject.html')
        # POST, user with good permission and correct form
        # -> redirect view to itself
        form_data = {'grade': 4, 'weight': 7,'student': self.student.user.id}
        self.assertTrue(AddGradeForm(form_data).is_valid())
        response = self.client_2.post(
            reverse(
                'yourgrades:teacher_subject',
                kwargs={'subject_unique_code': self.subject.unique_code}
            ),
            form_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,'/yourgrades/teachersubject/' + self.subject.unique_code
        )
        # Checking creation mail with info about new grade
        self.assertTrue(
            MailboxReceived.objects.filter(sender__user=self.teacher.user))


class CreateMessageViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)
        self.teacher = create_person('teacher', self.password)
        self.teacher.first_login = False
        self.teacher.save()
        self.client_2 = Client()
        self.client_2.login(username=self.teacher.user.username,
                            password=self.password)
        self.student = create_person('student', self.password)

    def test_create_message(self):
        # GET, user without student/parent/teacher/manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:create_message',
                kwargs={'prefix': 1, 'code': '2c2020'}
            )
        )
        self.assertEqual(response.status_code, 403)
        # GET, user with student/parent/teacher/manager permission -> 200
        response = self.client_2.get(
            reverse(
                'yourgrades:create_message',
                kwargs={'prefix': 4, 'code': self.student.user.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/message.html')
        # POST, user with student/parent/teacher/manager permission and correct
        # form -> redirect to assigned (student_parent/teacher/manager)
        # panel view
        form_data = {'subject': 'Some subject', 'text': 'Some text.'}
        self.assertTrue(MessageForm(form_data).is_valid())
        response = self.client_2.post(
            reverse(
                'yourgrades:create_message',
                kwargs={'prefix': 4, 'code': self.student.user.id}
            ),
            form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/yourgrades/teacher')
        # Checking mail creation
        self.assertTrue(
            MailboxReceived.objects.filter(sender__user=self.teacher.user,
                                           recipient__user=self.student.user))
        message = MailboxReceived.objects.get(
            sender__user=self.teacher.user,
            recipient__user=self.student.user
        ).message
        self.assertEqual(message.subject, 'Some subject')
        self.assertEqual(message.text, 'Some text.')


class MailboxViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)
        self.parent = create_person('parent', self.password)
        self.client_2 = Client()
        self.client_2.login(username=self.parent.user.username,
                            password=self.password)

    def test_mailbox(self):
        # GET, user without student/parent/teacher/manager permission -> 403
        response = self.client_1.get(reverse('yourgrades:mailbox'))
        self.assertEqual(response.status_code, 403)
        # GET, user with student/parent/teacher/manager permission -> 200
        response = self.client_2.get(reverse('yourgrades:mailbox'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/mailbox.html')


class MailTextViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)
        self.student = create_person('student', self.password)
        self.client_2 = Client()
        self.client_2.login(username=self.student.user.username,
                            password=self.password)
        self.teacher = create_person('teacher', self.password)
        message = Message.objects.create(subject='Test subject',
                                         text='Test text.')
        recipient = Recipient.objects.create(user=self.student.user,
                                             message=message)
        sender = Sender.objects.create(user=self.teacher.user, message=message)
        self.mailbox_received = MailboxReceived.objects.create(
            sender=sender,
            recipient=recipient,
            message=message,
        )

    def test_mailbox(self):
        # GET, user without student/parent/teacher/manager permission -> 403
        response = self.client_1.get(reverse('yourgrades:mail_text', kwargs={
            'mailbox_id': self.mailbox_received.id, 'mailbox_type': 1}))
        self.assertEqual(response.status_code, 403)
        # GET, user with student/parent/teacher/manager permission -> 200

        # Mailbox type 1 (received)
        response = self.client_2.get(reverse('yourgrades:mail_text', kwargs={
            'mailbox_id': self.mailbox_received.id, 'mailbox_type': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/mailtext.html')
        # Checking if message is read
        self.assertEqual(
            MailboxReceived.objects.get(id=self.mailbox_received.id).read,
            True)

        # Mailbox type 2 (sent)
        new_message = Message.objects.create(subject='Test subject 2',
                                             text='Test text 2.')
        mailbox_sent = MailboxSent.objects.create(
            sender=Sender.objects.create(
                user=self.student.user,
                message=new_message
            ),
            recipient='Jan Kowalski',
            message=new_message
        )
        response = self.client_2.get(reverse('yourgrades:mail_text', kwargs={
            'mailbox_id': mailbox_sent.id, 'mailbox_type': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/mailtext.html')


class StudentParentViewTestCase(TestCase):
    password = 'testerspass'

    def setUp(self):
        user = create_user(self.password)
        self.client_1 = Client()
        self.client_1.login(username=user.username,
                            password=self.password)
        self.parent = create_person('parent', self.password)
        self.parent.first_login = False
        self.parent.save()
        self.client_2 = Client()
        self.client_2.login(username=self.parent.user.username,
                            password=self.password)
        self.student = create_person('student', self.password)
        self.student.first_login = False
        self.student.save()
        self.client_3 = Client()
        self.client_3.login(username=self.student.user.username,
                            password=self.password)

    def test_mailbox(self):
        # GET, user without student/parent/ permission -> 403
        response = self.client_1.get(reverse('yourgrades:student_parent'))
        self.assertEqual(response.status_code, 403)

        # GET, user with parent permission -> 200
        response = self.client_2.get(reverse('yourgrades:student_parent'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/studentparent.html')
        # Checking user type (parent/student)
        self.assertEqual(response.context['person'], self.parent)

        # GET, user with student permission -> 200
        response = self.client_3.get(reverse('yourgrades:student_parent'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/studentparent.html')
        # Checking user type (parent/student)
        self.assertEqual(response.context['person'], self.student)
