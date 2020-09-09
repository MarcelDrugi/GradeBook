from datetime import datetime
from django.test import TestCase
import pytz
from django.contrib.auth.models import User

from yourgrades.models import SchoolClass, Student, Parent, Teacher, Subject, \
    SubjectTeachers, SubjectDate, Grades, CanceledGrades, Message, Sender, \
    Recipient, MailboxReceived, MailboxSent


class SchoolClassTestCase(TestCase):
    def setUp(self):
        self.school_class_data = {
            'unique_code': '1a2020',
            'name': '1a',
            'year': 2020
        }
        SchoolClass.objects.create(**self.school_class_data)

    def test_school_class(self):
        school_class = SchoolClass.objects.get(
            unique_code=self.school_class_data['unique_code']
        )
        self.assertTrue(isinstance(school_class, SchoolClass))
        self.assertEqual(school_class.unique_code[0:2], school_class.name)
        self.assertEqual(school_class.unique_code[2:6], str(school_class.year))
        self.assertEqual(
            school_class.unique_code,
            self.school_class_data['unique_code']
        )


class StudentTestCase(TestCase):
    def setUp(self):
        self.user_data = {'username': 'AdamNowak', 'password': 'adamspass'}
        user = User.objects.create_user(**self.user_data)
        school_class_data = {
            'unique_code': '1b2020',
            'name': '1b',
            'year': 2020
        }
        school_class = SchoolClass.objects.create(**school_class_data)
        Student.objects.create(
            user=user,
            school_class=school_class,
            name='Adam',
            surname='Nowak',
            birthday='2011-03-29',
            email='jankowalski@example.pl'
        )

    def test_student(self):
        student = Student.objects.get(
            user__username=self.user_data['username']
        )
        self.assertTrue(isinstance(student, Student))
        self.assertEqual(student.first_login, True)
        self.assertEqual(
            student.__str__(),
            f'{student.name} {student.surname}'
        )
        self.assertEqual(
            student.school_class,
            SchoolClass.objects.last()
        )


class ParentTestCase(TestCase):
    def setUp(self):
        student_user_data = {'username': 'JanNowak', 'password': 'janspass'}
        student_user = User.objects.create_user(**student_user_data)
        school_class_data = {
            'unique_code': '1c2020',
            'name': '1c',
            'year': 2020
        }
        SchoolClass.objects.create(**school_class_data)
        school_class = SchoolClass.objects.get(
            unique_code=school_class_data['unique_code']
        )
        self.student = Student.objects.create(
            user=student_user,
            school_class=school_class,
            name='Adam',
            surname='Nowak',
            birthday='2011-03-29',
            email='jankowalski@example.pl'
        )

        self.parent_user_data = {
            'username': 'AnnaNowak',
            'password': 'annaspass'
        }
        parent_user = User.objects.create_user(**self.parent_user_data)
        self.parent_data = {
            'user': parent_user,
            'student': self.student,
            'name': 'Anna',
            'surname': 'Nowak'
        }
        Parent.objects.create(**self.parent_data)

    def test_parent(self):
        parent = Parent.objects.get(
            user__username=self.parent_user_data['username']
        )
        self.assertTrue(isinstance(parent, Parent))
        self.assertEqual(parent.first_login, True)
        self.assertTrue(parent.student, self.student)
        self.assertEqual(parent.name, self.parent_data['name'])
        self.assertEqual(parent.surname, self.parent_data['surname'])
        self.assertEqual(parent.__str__(), f'{parent.name} {parent.surname}')


class TeacherTestCase(TestCase):
    def setUp(self):
        self.teacher_user_data = {
            'username': 'KarolNowak',
            'password': 'karospass'
        }
        self.teacher_user = User.objects.create_user(**self.teacher_user_data)
        self.teacher_data = {
            'user': self.teacher_user,
            'name': 'Karol',
            'surname': 'Nowak',
            'email': 'karolnowak@example.pl'
        }
        Teacher.objects.create(**self.teacher_data)

    def test_teacher(self):
        teacher = Teacher.objects.get(
            user__username=self.teacher_user_data['username']
        )
        self.assertTrue(isinstance(teacher, Teacher))
        self.assertEqual(teacher.first_login, True)
        self.assertEqual(teacher.active, True)
        self.assertEqual(teacher.user, self.teacher_user)
        self.assertEqual(teacher.name, self.teacher_data['name'])
        self.assertEqual(teacher.surname, self.teacher_data['surname'])
        self.assertEqual(teacher.email, self.teacher_data['email'])
        self.assertEqual(
            teacher.__str__(),
            f'{teacher.name} {teacher.surname}'
        )


class SubjectTestCase(TestCase):
    def setUp(self):
        self.school_class_data = {
            'unique_code': '1d2020',
            'name':  '1d',
            'year': 2020
        }
        self.school_class = SchoolClass.objects.create(**self.school_class_data)
        self.subject_data = {
            'name': 'History',
            'unique_code': 'Hi1d2020',
            'school_class': self.school_class
        }
        Subject.objects.create(**self.school_class_data)

    def subject_test(self):
        subject = Subject.object.get(name=self.subject_data['name'])
        self.assertTrue(isinstance(subject, Subject))
        self.assertEqual(len(subject.unique_code), 8)
        self.assertEqual(subject.__str__(), subject.name)
        self.assertEqual(subject.unique_code, self.subject_data['unique_code'])
        self.assertEqual(subject.school_class, self.school_class)


class SubjectTeacherTestCase(TestCase):
    def setUp(self):
        self.school_class = SchoolClass.objects.create(
            unique_code='1e2020',
            name='1e',
            year=2020
        )
        self.subject_data = {
            'name': 'Chemistry',
            'unique_code': 'Ch1e2020',
            'school_class': self.school_class
        }
        self.subject = Subject.objects.create(**self.subject_data)
        teacher_user_data = {'username': 'MarcinNowak',
                             'password': 'marcinspass'}
        teacher_user = User.objects.create_user(**teacher_user_data)
        self.teacher = Teacher.objects.create(
            user=teacher_user,
            name='Marcin',
            surname='Nowak',
            email='marcinnowak@example.pl'
        )
        self.subject_teacher = SubjectTeachers.objects.create(
            subject=self.subject
        )
        self.subject_teacher.teacher.add(self.teacher)

    def test_subject_teachers(self):
        subject_teachers = SubjectTeachers.objects.get(
            subject__unique_code=self.subject_data['unique_code']
        )
        self.assertTrue(isinstance(subject_teachers, SubjectTeachers))
        self.assertEqual(subject_teachers.teacher.last(), self.teacher)
        self.assertEqual(subject_teachers.subject, self.subject)


class SubjectDateTestCase(TestCase):
    def setUp(self):
        school_class = SchoolClass.objects.create(
            unique_code='4e2020',
            name='4e',
            year=2020
        )
        self.subject = Subject.objects.create(
            name='Biology',
            unique_code='Bi4e2020',
            school_class=school_class
        )
        self.subject_date_data = {
            'day': 'Mo',
            'lesson_number': 4,
            'subject': self.subject,
        }
        SubjectDate.objects.create(**self.subject_date_data)

    def test_subject_date(self):
        subject_date = SubjectDate.objects.get(
            subject=self.subject
        )
        self.assertTrue(isinstance(subject_date, SubjectDate))
        self.assertIn(subject_date.day, dict(SubjectDate.DAYS))
        self.assertLessEqual(
            subject_date.lesson_number,
            sorted(SubjectDate.LESSONS)[-1][0])
        self.assertGreaterEqual(
            subject_date.lesson_number,
            sorted(SubjectDate.LESSONS)[0][0]
        )


class GradesTestCase(TestCase):
    def setUp(self):
        user_data = {'username': 'MarekNowak', 'password': 'marekspass'}
        user = User.objects.create_user(**user_data)
        school_class_data = {
            'unique_code': '1f2020',
            'name': '1f',
            'year': 2020
        }
        school_class = SchoolClass.objects.create(**school_class_data)
        self.student = Student.objects.create(
            user=user,
            school_class=school_class,
            name='Marek', surname='Nowak',
            birthday='2011-04-11',
            email='mareknowak@example.pl'
        )
        self.subject = Subject.objects.create(
            name='Maths',
            unique_code='Ma1d2020',
            school_class=school_class
        )
        self.grade_data = {
            'weight': 8,
            'grade': 5,
            'student': self.student,
            'subject': self.subject,
        }
        Grades.objects.create(**self.grade_data)

    def test_grades(self):
        grade = Grades.objects.last()
        self.assertTrue(isinstance(grade, Grades))
        now = pytz.utc.localize(datetime.now())
        self.assertTrue(grade.date <= now)
        self.assertTrue(1 <= grade.weight <= 10)
        self.assertTrue(1 <= grade.grade <= 6)
        self.assertEqual(grade.weight, self.grade_data['weight'])
        self.assertEqual(grade.grade, self.grade_data['grade'])
        self.assertEqual(grade.student, self.student)
        self.assertEqual(grade.subject, self.subject)


class CanceledGradesTestCase(TestCase):
    def setUp(self):
        user_data = {'username': 'KamilNowak', 'password': 'kamilspass'}
        user = User.objects.create_user(**user_data)
        school_class_data = {
            'unique_code': '1g2020',
            'name': '1g',
            'year': 2020
        }
        school_class = SchoolClass.objects.create(**school_class_data)
        self.student = Student.objects.create(
            user=user,
            school_class=school_class,
            name='Kamil',
            surname='Nowak',
            birthday='2010-04-11',
            email='kamilnowak@example.pl'
        )
        self.subject = Subject.objects.create(
            name='Gym',
            unique_code='Gy1d2020',
            school_class=school_class
        )
        self.canceled_grade_data = {
            'weight': 9,
            'grade': 4,
            'student': self.student,
            'subject': self.subject,
        }
        CanceledGrades.objects.create(**self.canceled_grade_data)

    def test_grades(self):
        canceled_grade = CanceledGrades.objects.last()
        self.assertTrue(isinstance(canceled_grade, CanceledGrades))
        now = pytz.utc.localize(datetime.now())
        self.assertTrue(canceled_grade.date <= now)
        self.assertTrue(1 <= canceled_grade.weight <= 10)
        self.assertTrue(1 <= canceled_grade.grade <= 6)
        self.assertEqual(
            canceled_grade.weight,
            self.canceled_grade_data['weight']
        )
        self.assertEqual(
            canceled_grade.grade,
            self.canceled_grade_data['grade']
        )
        self.assertEqual(canceled_grade.student, self.student)
        self.assertEqual(canceled_grade.subject, self.subject)


class MessageTestCase(TestCase):
    def setUp(self):
        self.message_data = {
            'id': 1,
            'subject': 'Test subject',
            'text': 'Test text.',
        }
        Message.objects.create(**self.message_data)

    def test_message(self):
        message = Message.objects.get(id=self.message_data['id'])
        self.assertTrue(isinstance(message, Message))
        now = pytz.utc.localize(datetime.now())
        self.assertTrue(message.date <= now)

        max_text_length = message._meta.get_field('text').max_length
        self.assertEqual(max_text_length, 1024)
        self.assertLessEqual(len(message.text), max_text_length)

        max_subject_length = message._meta.get_field('subject').max_length
        self.assertEqual(max_subject_length, 128)
        self.assertLessEqual(len(message.subject), max_subject_length)


class MailTestCase(TestCase):
    def setUp(self):
        self.message = Message.objects.create(
            id=1,
            subject='Test subject',
            text='Test text.'
        )

        sender_user_data = {
            'username': 'JanMalinowski',
            'first_name': 'Jan',
            'last_name': 'Malinowski',
            'password': 'janspass'
        }
        self.sender_user = User.objects.create_user(**sender_user_data)
        self.sender = Sender.objects.create(
            user=self.sender_user,
            message=self.message
        )

        recipient_user_data = {
            'username': 'AdamKowalski',
            'first_name': 'Adam',
            'last_name': 'Kowalski',
            'password': 'adamspass'
        }
        self.recipient_user = User.objects.create_user(**recipient_user_data)
        self.recipient = Recipient.objects.create(
            user=self.recipient_user,
            message=self.message
        )


class SenderTestCse(MailTestCase):
    def setUp(self):
        super(SenderTestCse, self).setUp()

    def test_sender(self):
        sender = Sender.objects.last()
        self.assertTrue(isinstance(sender, Sender))
        self.assertEqual(
            sender.__str__(),
            f'{sender.user.first_name} {sender.user.last_name}'
        )
        self.assertEqual(sender.user, self.sender_user)
        self.assertEqual(sender.message, self.message)


class RecipientTestCase(MailTestCase):
    def setUp(self):
        super(RecipientTestCase, self).setUp()

    def test_recipient(self):
        recipient = Recipient.objects.last()
        self.assertTrue(isinstance(recipient, Recipient))
        self.assertEqual(
            recipient.__str__(),
            f'{recipient.user.first_name} {recipient.user.last_name}'
        )
        self.assertEqual(recipient.user, self.recipient_user)
        self.assertEqual(recipient.message, self.message)


class MailboxReceivedTestCase(MailTestCase):
    def setUp(self):
        super(MailboxReceivedTestCase, self).setUp()
        self.mailbox_data = {
            'sender': self.sender,
            'recipient': self.recipient,
            'message': self.message,
        }
        MailboxReceived.objects.create(**self.mailbox_data)

    def test_mailbox_received(self):
        mailbox_received = MailboxReceived.objects.last()
        self.assertTrue(isinstance(mailbox_received, MailboxReceived))
        self.assertEqual(mailbox_received.read, False)
        self.assertEqual(mailbox_received.recipient, self.recipient)


class MailboxSentTestCase(MailTestCase):
    def setUp(self):
        super(MailboxSentTestCase, self).setUp()
        self.mailbox_sent_data = {
            'sender': self.sender,
            'recipient': 'Some recipient',
            'message': self.message,
        }
        MailboxSent.objects.create(**self.mailbox_sent_data)

    def test_mailbox_received(self):
        mailbox_sent = MailboxSent.objects.last()
        self.assertTrue(isinstance(mailbox_sent, MailboxSent))

        max_length = mailbox_sent._meta.get_field('recipient').max_length
        self.assertEqual(max_length, 64)
        self.assertLessEqual(len(mailbox_sent.recipient), max_length)

        self.assertEqual(mailbox_sent.sender, self.sender)
        self.assertEqual(mailbox_sent.message, self.message)

