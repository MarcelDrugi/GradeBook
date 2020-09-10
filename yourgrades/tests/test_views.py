""" Views and forms tests """
from django.shortcuts import get_object_or_404
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from yourgrades.forms import *


class TestWithPermission(TestCase):
    """
    Base class for all tests of views that require user authorization.
    """
    def setUp(self):
        self.password = 'test_pass'

    def create_user(self):
        username = 'tester'
        numbering = 0
        while True:
            try:
                User.objects.get(username=username)
                numbering += 1
                username += str(numbering)
            except User.DoesNotExist:
                return User.objects.create_user(
                    username=username,
                    password=self.password,
                    first_name='Name',
                    last_name='Surname'
                )

    def create_person(self, kind):
        content_type = ContentType.objects.get_for_model(RightsSupport)
        permission = Permission.objects.get(
            content_type=content_type,
            codename=kind
        )
        if kind in {'student', 'parent'}:
            user = self.create_user()
            user.user_permissions.add(permission)
            try:
                school_class = SchoolClass.objects.get(unique_code='2a2020')
            except SchoolClass.DoesNotExist:
                school_class = SchoolClass.objects.create(
                    unique_code='2a2020',
                    name='2a',
                    year=2020
                )
            student = Student.objects.create(
                user=user,
                school_class=school_class,
                name=user.first_name,
                surname=user.last_name,
                birthday='2010-03-29'
            )
            if kind == 'student':
                return student
            if kind == 'parent':
                user = self.create_user()
                user.user_permissions.add(permission)
                return Parent.objects.create(
                    user=user,
                    student=student,
                    name=user.first_name,
                    surname=user.last_name
                )
        if kind == 'teacher':
            user = self.create_user()
            user.user_permissions.add(permission)
            return Teacher.objects.create(
                user=user,
                name=user.first_name,
                surname=user.last_name
            )

    def create_manager(self):
        user = self.create_user()
        content_type = ContentType.objects.get_for_model(RightsSupport)
        permission = Permission.objects.get(
            content_type=content_type,
            codename='manager'
        )
        user.user_permissions.add(permission)
        return user


class HomepageViewTestCase(TestWithPermission):
    def setUp(self):
        super(HomepageViewTestCase, self).setUp()
        # Create users and student/parent/teacher models objects to test login
        # by homepage
        self.student_1 = self.create_person('student')
        self.student_1_form_data = {
            'username': self.student_1.user.username,
            'password': self.password
        }
        self.student_2 = self.create_person('student')
        self.student_2.first_login = False
        self.student_2.save()
        self.student_2_form_data = {
            'username': self.student_2.user.username,
            'password': self.password
        }

        self.parent_1 = self.create_person('parent')
        self.parent_1_form_data = {
            'username': self.parent_1.user.username,
            'password': self.password
        }
        self.parent_2 = self.create_person('parent')
        self.parent_2.first_login = False
        self.parent_2.save()
        self.parent_2_form_data = {
            'username': self.parent_2.user.username,
            'password': self.password
        }

        self.teacher_1 = self.create_person('teacher')
        self.teacher_1_form_data = {
            'username': self.teacher_1.user.username,
            'password': self.password
        }
        self.teacher_2 = self.create_person('teacher')
        self.teacher_2.first_login = False
        self.teacher_2.save()
        self.teacher_2_form_data = {
            'username': self.teacher_2.user.username,
            'password': self.password
        }

    def test_homepage_view(self):
        response = Client().get(reverse('yourgrades:homepage'))
        self.assertEqual(response.status_code, 200)

        # Post with clean form or with wrong data -> no redirects
        response = Client().post(reverse('yourgrades:homepage'))
        self.assertEqual(response.status_code, 200)
        response = Client().post(
            reverse('yourgrades:homepage'),
            {
                'username': 'tester',
                'password': 'wrongpass'
            }
        )
        self.assertEqual(response.status_code, 200)

        # Student redirection tests
        # if first_login field is True -> redirects to FirstLoginView
        self.assertTrue(LoginForm(self.student_1_form_data).is_valid())
        response = Client().post(
            reverse('yourgrades:homepage'),
            self.student_1_form_data,
        )
        self.assertEqual(response.status_code, 302)
        response = Client().post(
            reverse('yourgrades:homepage'),
            self.student_1_form_data,
            follow=True
        )
        self.assertRedirects(response, '/yourgrades/firstlogin')

        # if first_login field is False, redirects to StudentParentView
        self.assertTrue(LoginForm(self.student_2_form_data).is_valid())
        response = Client().post(
            reverse('yourgrades:homepage'),
            self.student_2_form_data,
        )
        self.assertEqual(response.status_code, 302)
        response = Client().post(
            reverse('yourgrades:homepage'),
            self.student_2_form_data,
            follow=True
        )
        self.assertRedirects(response, '/yourgrades/studentparent')
        self.assertTemplateUsed(response, 'yourgrades/studentparent.html')

        # Parent redirection tests
        # if first_login field is True, redirects to FirstLoginView
        self.assertTrue(LoginForm(self.parent_1_form_data).is_valid())
        response = Client().post(
            reverse('yourgrades:homepage'),
            self.parent_1_form_data,
        )
        self.assertEqual(response.status_code, 302)
        response = Client().post(
            reverse('yourgrades:homepage'),
            self.parent_1_form_data,
            follow=True
        )
        self.assertRedirects(response, '/yourgrades/firstlogin')

        # if first_login field is False, redirects to StudentParentView
        self.assertTrue(LoginForm(self.parent_2_form_data).is_valid())
        response = Client().post(
            reverse('yourgrades:homepage'),
            self.parent_2_form_data,
        )
        self.assertEqual(response.status_code, 302)
        response = Client().post(
            reverse('yourgrades:homepage'),
            self.parent_2_form_data,
            follow=True
        )
        self.assertRedirects(response, '/yourgrades/studentparent')
        self.assertTemplateUsed(response, 'yourgrades/studentparent.html')

        # Teacher redirection tests
        # if first_login field is True, redirects to FirstLoginView
        self.assertTrue(LoginForm(self.teacher_1_form_data).is_valid())
        response = Client().post(
            reverse('yourgrades:homepage'),
            self.teacher_1_form_data,
        )
        self.assertEqual(response.status_code, 302)
        response = Client().post(
            reverse('yourgrades:homepage'),
            self.teacher_1_form_data,
            follow=True
        )
        self.assertRedirects(response, '/yourgrades/firstlogin')

        # if first_login field is False, redirects to TeacherPanelView
        self.assertTrue(LoginForm(self.teacher_2_form_data).is_valid())
        response = Client().post(
            reverse('yourgrades:homepage'),
            self.teacher_2_form_data,
        )
        self.assertEqual(response.status_code, 302)
        response = Client().post(
            reverse('yourgrades:homepage'),
            self.teacher_2_form_data,
            follow=True
        )
        self.assertRedirects(response, '/yourgrades/teacher')
        self.assertTemplateUsed(response, 'yourgrades/teacher.html')


class LogOutViewTestCase(TestWithPermission):
    def setUp(self):
        super(LogOutViewTestCase, self).setUp()
        password = 'testerspass'
        user = self.create_user()
        self.client = Client()
        self.client.login(username=user.username, password=password)

    def test_logout(self):
        response = self.client.get(reverse('yourgrades:logout'))
        self.assertEqual(response.status_code, 302)
        # Logout redirects to homepage
        response = self.client.get(reverse('yourgrades:logout'), follow=True)
        self.assertRedirects(response, '/yourgrades')


class FirstLoginViewTestCase(TestWithPermission):

    def setUp(self):
        super(FirstLoginViewTestCase, self).setUp()
        no_perm_user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=no_perm_user.username,
            password=self.password
        )
        # Create Student (with assigned User) and logging him in
        self.student = self.create_person('student')
        self.client_2 = Client()
        self.client_2.login(
            username=self.student.user.username,
            password=self.password
        )

    def test_first_login(self):
        # GET, user without permission -> 403
        response = self.client_1.get(reverse('yourgrades:first_login'))
        self.assertEqual(response.status_code, 403)

        # GET, user with permission -> 200
        response = self.client_2.get(reverse('yourgrades:first_login'))
        self.assertEqual(response.status_code, 200)

        # POST with wrong form data (or no form data) -> no redirection
        response = self.client_2.post(
            reverse('yourgrades:first_login'),
            {
                'username': '',
                'password': 'anything',
                'password_confirm': 'incorrect'
            }
        )
        self.assertEqual(response.status_code, 200)

        # POST, user with good permission and correct form
        # -> redirection to assigned panel
        form_data = {
            'username': 'newusername',
            'password': 'newpass',
            'password_confirm': 'newpass'
        }
        self.assertTrue(FirstLoginForm(form_data).is_valid())
        response = self.client_2.post(
            reverse('yourgrades:first_login'),
            form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/yourgrades/studentparent')
        response = self.client_2.post(
            reverse('yourgrades:first_login'),
            form_data,
            follow=True
        )
        self.assertTemplateUsed(response, 'yourgrades/studentparent.html')


class ManagerPanelViewTestCase(TestWithPermission):

    def setUp(self):
        super(ManagerPanelViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )

    def test_manager_panel(self):
        # User without manager permission -> 403
        response = self.client_1.get(reverse('yourgrades:manager'))
        self.assertEqual(response.status_code, 403)

        # User with manager permission -> 200
        response = self.client_2.get(reverse('yourgrades:manager'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/manager.html')


class CreateSchoolClassViewTestCase(TestWithPermission):

    def setUp(self):
        super(CreateSchoolClassViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )

    def test_create_school_class(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(reverse('yourgrades:create_school_class'))
        self.assertEqual(response.status_code, 403)

        # GET, user with manager permission -> 200
        response = self.client_2.get(reverse('yourgrades:create_school_class'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'yourgrades/managercreateschoolclass.html'
        )

        # POST with wrong form data (or no form data) -> no redirection
        response = self.client_2.post(
            reverse('yourgrades:create_school_class'),
            {'name': '2b', 'year': 2020, 'unique_code': 'wrong_code'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'yourgrades/managercreateschoolclass.html'
        )

        # POST, user with good permission and correct form
        # -> redirect to manager view
        form_data = {'name': '2b', 'year': 2020, 'unique_code': '2b2020'}
        self.assertTrue(SchoolClassForm(form_data).is_valid())
        response = self.client_2.post(
            reverse('yourgrades:create_school_class'),
            form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/yourgrades/manager')
        response = self.client_2.post(
            reverse('yourgrades:create_school_class'),
            form_data,
            follow=True
        )
        self.assertTemplateUsed(
            response,
            'yourgrades/managercreateschoolclass.html'
        )

        # Check school class creation
        self.assertEqual(
            SchoolClass.objects.filter(
                unique_code=form_data['unique_code']
            ).count(),
            1
        )


class EditSchoolClassViewTestCase(TestWithPermission):

    def setUp(self):
        super(EditSchoolClassViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )
        self.class_data = {'name': '2c', 'year': 2020, 'unique_code': '2c2020'}
        SchoolClass.objects.create(**self.class_data)

    def test_edit_school_class(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:edit_school_class',
                kwargs={'class_unique_code': self.class_data['unique_code']}
            )
        )
        self.assertEqual(response.status_code, 403)

        # GET, user with manager permission -> 200
        response = self.client_2.get(
            reverse(
                'yourgrades:edit_school_class',
                kwargs={'class_unique_code': self.class_data['unique_code']}
            )
        )
        self.assertEqual(response.status_code, 200)

        # POST with wrong form data (or no form data) -> no redirection
        response = self.client_2.post(
            reverse(
                'yourgrades:edit_school_class',
                kwargs={'class_unique_code': self.class_data['unique_code']}
            ),
            {
                'name': 'Jan',
                'surname': '',  # no surname
                'birthday': '2011-10-14',
                'first_parent_name': 'Adam',
                'first_parent_surname': 'Kowalski'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'yourgrades/managereditschoolclass.html'
        )

        # POST, user with good permission and correct form
        # -> redirect view to itself
        form_data = {
            'name': 'Jan',
            'surname': 'Kowalski',
            'birthday': '2011-10-14',
            'first_parent_name': 'Adam',
            'first_parent_surname': 'Kowalski'
        }
        self.assertTrue(CreateStudentForm(form_data).is_valid())
        response = self.client_2.post(
            reverse(
                'yourgrades:edit_school_class',
                kwargs={'class_unique_code': self.class_data['unique_code']}
            ),
            form_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            '/yourgrades/manager/editschoolclass/2c2020'
        )
        self.assertTemplateUsed(
            response,
            'yourgrades/managereditschoolclass.html'
        )
        # Check student and parent creation
        self.assertEqual(
            Student.objects.filter(
                name=form_data['name'],
                surname=form_data['surname']
            ).count(),
            1
        )
        self.assertEqual(
            Parent.objects.filter(
                name=form_data['first_parent_name'],
                surname=form_data['first_parent_surname']
            ).count(),
            1
        )


class DeactivationSchoolClassViewTestCase(TestWithPermission):

    def setUp(self):
        super(DeactivationSchoolClassViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )
        self.class_data = {'name': '2c', 'year': 2020, 'unique_code': '2c2020'}
        SchoolClass.objects.create(**self.class_data)

    def test_deactivation_school_class(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:deactivation_school_class',
                kwargs={'class_unique_code': self.class_data['unique_code']}
            )
        )
        self.assertEqual(response.status_code, 403)

        # GET, user with permission -> 405
        response = self.client_2.get(
            reverse(
                    'yourgrades:deactivation_school_class',
                    kwargs={
                        'class_unique_code': self.class_data['unique_code']
                    }
            )
        )
        self.assertEqual(response.status_code, 405)

        # POST, user with good permission redirect to edit_school_class view
        response = self.client_2.post(
            reverse(
                'yourgrades:deactivation_school_class',
                kwargs={'class_unique_code': self.class_data['unique_code']}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '/yourgrades/manager/editschoolclass/' +
            self.class_data['unique_code']
        )
        # Check class deactivation
        school_class = SchoolClass.objects.get(
            unique_code=self.class_data['unique_code']
        )
        self.assertEqual(school_class.active, False)


class DeactivationTeacherViewTestCase(TestWithPermission):

    def setUp(self):
        super(DeactivationTeacherViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )
        self.teacher = self.create_person('teacher')

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


class ActivationSchoolClassViewTestCase(TestWithPermission):

    def setUp(self):
        super(ActivationSchoolClassViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )
        self.class_data = {
            'name': '2c',
            'year': 2020,
            'unique_code': '2c2020',
            'active': False,
        }
        SchoolClass.objects.create(**self.class_data)

    def test_activation_school_class(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:activation_school_class',
                kwargs={'class_unique_code': self.class_data['unique_code']}
            )
        )
        self.assertEqual(response.status_code, 403)

        # GET, user with permission -> 405
        response = self.client_2.get(
            reverse(
                'yourgrades:activation_school_class',
                kwargs={'class_unique_code': self.class_data['unique_code']}
            )
        )
        self.assertEqual(response.status_code, 405)

        # POST, user with good permission redirect to edit_school_class view
        response = self.client_2.post(
            reverse(
                'yourgrades:activation_school_class',
                kwargs={'class_unique_code': self.class_data['unique_code']}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '/yourgrades/manager/editschoolclass/' +
            self.class_data['unique_code']
        )

        # Check class activation
        school_class = get_object_or_404(
            SchoolClass,
            unique_code=self.class_data['unique_code']
        )
        self.assertEqual(school_class.active, True)


class DeleteStudentViewTestCase(TestWithPermission):

    def setUp(self):
        super(DeleteStudentViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )
        self.parent = self.create_person('parent')

    def test_delete_student(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:del_student',
                kwargs={'user_id': self.parent.student.user.id}
            )
        )
        self.assertEqual(response.status_code, 403)

        # GET, user with manager permission
        # -> redirect to edit_school_class view
        response = self.client_2.get(
            reverse(
                'yourgrades:del_student',
                kwargs={'user_id': self.parent.student.user.id}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '/yourgrades/manager/editschoolclass/' +
            self.parent.student.school_class.unique_code
        )

        # Check student deletion
        self.assertFalse(
            Student.objects.filter(user__id=self.parent.student.user.id)
        )


class AddTeacherViewTestCase(TestWithPermission):

    def setUp(self):
        super(AddTeacherViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )

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
            reverse('yourgrades:add_teacher'),
            {'name': '', 'surname': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'yourgrades/manageraddteacher.html'
        )

        # POST, user with good permission and correct form
        # -> redirect to manager view
        form_data = {'name': 'Anna', 'surname': 'Malinowska'}
        self.assertTrue(CreateTeacherForm(form_data).is_valid())
        response = self.client_2.post(
            reverse('yourgrades:add_teacher'),
            form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/yourgrades/manager')
        response = self.client_2.post(
            reverse('yourgrades:add_teacher'),
            form_data,
            follow=True
        )
        self.assertTemplateUsed(response, 'yourgrades/manager.html')


class AddSubjectViewTestCase(TestWithPermission):

    def setUp(self):
        super(AddSubjectViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )
        self.class_data = {'name': '2c', 'year': 2020, 'unique_code': '2c2020'}
        self.school_class = SchoolClass.objects.create(**self.class_data)
        self.teacher = self.create_person('teacher')

    def test_add_teacher(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:add_subject',
                kwargs={'class_unique_code': self.school_class.unique_code}
            )
        )
        self.assertEqual(response.status_code, 403)

        # GET, user with manager permission -> 200
        response = self.client_2.get(
            reverse(
                'yourgrades:add_subject',
                kwargs={'class_unique_code': self.school_class.unique_code}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/manageraddsubject.html')

        # POST with wrong form data (or no form data) -> no redirection
        response = self.client_2.post(
            reverse(
                'yourgrades:add_subject',
                kwargs={'class_unique_code': self.school_class.unique_code}
            ),
            {'name': 'Physics', 'shortcut': '', 'teachers': ''}  # no shortcut
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/manageraddsubject.html')

        # POST, user with good permission and correct form
        # -> redirect to edit_school_class view
        form_data = {'name': 'Physics', 'shortcut': 'Ph', }
        self.assertTrue(CreateSubjectForm(form_data).is_valid())
        response = self.client_2.post(
            reverse(
                'yourgrades:add_subject',
                kwargs={'class_unique_code': self.school_class.unique_code}
            ),
            form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '/yourgrades/manager/editschoolclass/' +
            self.school_class.unique_code
        )

        # Check Subject and Subject_teacher objects creation
        self.assertTrue(Subject.objects.filter(name='Physics'))
        subject = Subject.objects.get(name='Physics')
        self.assertEqual(
            subject.unique_code,
            form_data['shortcut'] + self.school_class.unique_code
        )


class ManagerSubjectViewTestCase(TestWithPermission):

    def setUp(self):
        super(ManagerSubjectViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )
        self.school_class = SchoolClass.objects.create(
            name='3b',
            year=2020,
            unique_code='3b2020'
        )
        self.subject = Subject.objects.create(
            name='History',
            unique_code='Hi3b2020',
            school_class=self.school_class
        )

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
        self.assertTemplateUsed(
            response,
            'yourgrades/managersubjectpanel.html'
        )

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


class DeleteSubjectDateViewTestCase(TestWithPermission):

    def setUp(self):
        super(DeleteSubjectDateViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )
        self.school_class = SchoolClass.objects.create(
            name='5b',
            year=2020,
            unique_code='5b2020'
        )
        self.subject = Subject.objects.create(
            name='Gym',
            unique_code='Gy5b2020',
            school_class=self.school_class
        )
        self.date = SubjectDate.objects.create(
            subject=self.subject,
            day='Fr',
            lesson_number=5
        )

    def test_delete_subject_date(self):
        # GET,user without manager permission -> 403
        kwargs = {
            'class_unique_code': self.school_class.unique_code,
            'subject_unique_code': self.subject.unique_code,
            'day': 5,
            'lesson': self.date.lesson_number
        }
        response = self.client_1.get(
            reverse(
                'yourgrades:delete_date',
                kwargs=kwargs,
            )
        )
        self.assertEqual(response.status_code, 403)

        # GET, user with manager permission -> redirection subject_view
        response = self.client_2.get(
            reverse(
                'yourgrades:delete_date',
                kwargs=kwargs,
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '/yourgrades/manager/editschoolclass/' +
            self.school_class.unique_code + '/' + self.subject.unique_code
        )


class TimetableViewTestCase(TestWithPermission):

    def setUp(self):
        super(TimetableViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        self.teacher = self.create_person('teacher')
        self.client_2 = Client()
        self.client_2.login(
            username=self.teacher.user.username,
            password=self.password
        )

        self.student = self.create_person('student')
        self.client_3 = Client()
        self.client_3.login(
            username=self.student.user.username,
            password=self.password
        )

    def test_timetable(self):
        # GET, user without student/parent/teacher  permission -> 403
        response = self.client_1.get(
            reverse('yourgrades:timetable', kwargs={'person': 'student'})
        )
        self.assertEqual(response.status_code, 403)

        # GET, user with student/parent permission -> 200
        response = self.client_2.get(
            reverse('yourgrades:timetable', kwargs={'person': 'teacher'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/timetable.html')
        # Checking returned context
        self.assertEqual(response.context['person'], 'teacher')

        # GET, user with teacher permission -> 200
        response = self.client_3.get(
            reverse('yourgrades:timetable', kwargs={'person': 'student'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/timetable.html')
        # Checking returned context
        self.assertEqual(response.context['person'], 'student')


class ManagerStudentViewTestCase(TestWithPermission):

    def setUp(self):
        super(ManagerStudentViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )
        self.parent = self.create_person('parent')
        self.subject = Subject.objects.create(
            name='Maths',
            unique_code=f'Ma{self.parent.student.school_class.unique_code}',
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
        self.assertRedirects(
            response,
            f'/yourgrades/manager/student/{self.parent.student.user.id}'
        )

        # Checking Grades model object
        self.assertEqual(
            Grades.objects.filter(
                subject=self.subject,
                student=self.parent.student
            ).count(),
            1
        )


class ManagerGradesHistoryViewTestCase(TestWithPermission):

    def setUp(self):
        super(ManagerGradesHistoryViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )

    def test_delete_student(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(reverse('yourgrades:manager_history'))
        self.assertEqual(response.status_code, 403)

        # GET, user with manager permission -> 200
        response = self.client_2.get(reverse('yourgrades:manager_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/managerhistory.html')


class DeleteSubjectViewTestCase(TestWithPermission):

    def setUp(self):
        super(DeleteSubjectViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )
        self.school_class = SchoolClass.objects.create(
            name='4a',
            year=2020,
            unique_code='4a2020'
        )
        self.subject = Subject.objects.create(
            name='Gym',
            unique_code='Gy4a2020',
            school_class=self.school_class
        )

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
        self.assertRedirects(
            response,
            '/yourgrades/manager/editschoolclass/' +
            str(self.school_class.unique_code)
        )


class DeleteSubjectTeacherViewTestCase(TestWithPermission):

    def setUp(self):
        super(DeleteSubjectTeacherViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )
        self.school_class = SchoolClass.objects.create(
            name='4a',
            year=2020,
            unique_code='4a2020'
        )
        self.subject = Subject.objects.create(
            name='Gym',
            unique_code='Gy4a2020',
            school_class=self.school_class
        )
        self.teacher = self.create_person('teacher')
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
                kwargs={'class_unique_code': self.school_class.unique_code, }
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
                kwargs={'class_unique_code': self.school_class.unique_code, }
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '/yourgrades/manager/editschoolclass/' +
            str(self.school_class.unique_code))


class ManagerDeleteTeacherViewTestCase(TestWithPermission):

    def setUp(self):
        super(ManagerDeleteTeacherViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )
        self.teacher_1 = self.create_person('teacher')
        self.teacher_2 = self.create_person('teacher')

    def test_manager_delete_teacher(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:manager_del_teacher',
                kwargs={'teacher_user_id': self.teacher_1.user.id, }
            )
        )
        self.assertEqual(response.status_code, 403)

        # GET, user with manager permission -> redirect to manager view
        response = self.client_2.get(
            reverse(
                'yourgrades:manager_del_teacher',
                kwargs={'teacher_user_id': self.teacher_1.user.id, }
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/yourgrades/manager')
        response = self.client_2.get(
            reverse(
                'yourgrades:manager_del_teacher',
                kwargs={'teacher_user_id': self.teacher_2.user.id, }
            ),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/manager.html')


class ManagerResetUserViewTestCase(TestWithPermission):

    def setUp(self):
        super(ManagerResetUserViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )
        self.student = self.create_person('student')

    def test_reset_user(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:manager_reset_user',
                kwargs={'user_id': self.student.user.id, 'prefix': 123, }
            ),
            HTTP_REFERER=reverse(
                'yourgrades:edit_school_class',
                kwargs={
                    'class_unique_code': self.student.school_class.unique_code,
                }
            )
        )
        self.assertEqual(response.status_code, 403)

        # GET, user with manager permission -> redirect to manager view
        response = self.client_2.get(
            reverse(
                'yourgrades:manager_reset_user',
                kwargs={'user_id': self.student.user.id, 'prefix': 123, }
            ),
            HTTP_REFERER=reverse(
                'yourgrades:edit_school_class',
                kwargs={
                    'class_unique_code': self.student.school_class.unique_code,
                }
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '/yourgrades/manager/editschoolclass/' +
            str(self.student.school_class.unique_code)
        )
        response = self.client_2.get(
            reverse(
                'yourgrades:manager_reset_user',
                kwargs={'user_id': self.student.user.id, 'prefix': 123, }
            ),
            HTTP_REFERER=reverse(
                'yourgrades:edit_school_class',
                kwargs={
                    'class_unique_code': self.student.school_class.unique_code,
                }
            ),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'yourgrades/managereditschoolclass.html'
        )


class ManagerTeacherEditViewTestCase(TestWithPermission):

    def setUp(self):
        super(ManagerTeacherEditViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )
        self.teacher = self.create_person('teacher')

    def test_manager_teacher_edit(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:manager_teacher_edit',
                kwargs={'user_id': self.teacher.user.id, }
            )
        )
        self.assertEqual(response.status_code, 403)

        # GET, user with manager permission -> 200
        response = self.client_2.get(
            reverse(
                'yourgrades:manager_teacher_edit',
                kwargs={'user_id': self.teacher.user.id, }
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/managereditteacher.html')

        # POST with wrong form data (or no form data) -> no redirection
        response = self.client_2.post(
            reverse(
                'yourgrades:manager_teacher_edit',
                kwargs={'user_id': self.teacher.user.id, }
            ),
            {'name': '', 'surname': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/managereditteacher.html')

        # POST, user with good permission and correct form
        # -> redirect to manager view
        form_data = {'name': 'Some-name', 'surname': 'Some-surname'}
        self.assertTrue(CreateTeacherForm(form_data).is_valid())
        response = self.client_2.post(
            reverse(
                'yourgrades:manager_teacher_edit',
                kwargs={'user_id': self.teacher.user.id}
            ),
            form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '/yourgrades/manager/teacher/'
            + str(self.teacher.user.id)
        )
        response = self.client_2.post(
            reverse(
                'yourgrades:manager_teacher_edit',
                kwargs={'user_id': self.teacher.user.id}
            ),
            follow=True
        )
        self.assertTemplateUsed(response, 'yourgrades/managereditteacher.html')

        # Checking Teacher objects change
        self.assertEqual(
            Teacher.objects.filter(
                name=form_data['name'],
                surname=form_data['surname']
            ).count(),
            1
        )


class ManagerStudentEditViewTestCse(TestWithPermission):

    def setUp(self):
        super(ManagerStudentEditViewTestCse, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )
        self.parent = self.create_person('parent')

    def test_manager_student_edit(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:manager_student_edit',
                kwargs={'user_id': self.parent.student.user.id, }
            )
        )
        self.assertEqual(response.status_code, 403)
        # GET, user with manager permission -> 200
        response = self.client_2.get(
            reverse(
                'yourgrades:manager_student_edit',
                kwargs={'user_id': self.parent.student.user.id, }
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/managereditstudent.html')
        # POST, user with good permission and correct form
        # -> redirect to manager_student view
        form_data = {
            'name': 'Somename',
            'surname': 'Somesurname',
            'birthday': '2010-02-24',
            'first_parent_name': 'Othername',
            'first_parent_surname': 'Othersurname'
        }
        self.assertTrue(CreateStudentForm(form_data).is_valid())
        response = self.client_2.post(
            reverse(
                'yourgrades:manager_student_edit',
                kwargs={'user_id': self.parent.student.user.id}
            ),
            form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'/yourgrades/manager/student/{self.parent.student.user.id}'
        )


class AddSubjectTeacherViewTestCase(TestWithPermission):

    def setUp(self):
        super(AddSubjectTeacherViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )
        self.school_class = SchoolClass.objects.create(
            name='4a',
            year=2020,
            unique_code='4a2020'
        )
        self.subject = Subject.objects.create(
            name='History',
            unique_code='Hi4a2020',
            school_class=self.school_class
        )
        self.teacher = self.create_person('teacher')

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
        self.assertTemplateUsed(
            response,
            'yourgrades/manageraddsubjectteacher.html'
        )


class ManagerTeacherViewTestCase(TestWithPermission):

    def setUp(self):
        super(ManagerTeacherViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        user_manager = self.create_manager()
        self.client_2 = Client()
        self.client_2.login(
            username=user_manager.username,
            password=self.password
        )
        self.teacher = self.create_person('teacher')

    def test_manager_teacher(self):
        # GET,user without manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:manager_teacher',
                kwargs={'teacher_user_id': self.teacher.user.id, }
            )
        )
        self.assertEqual(response.status_code, 403)
        # GET, user with manager permission -> 200
        response = self.client_2.get(
            reverse(
                'yourgrades:manager_teacher',
                kwargs={'teacher_user_id': self.teacher.user.id, }
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/managerteacher.html')


class TeacherPanelViewTestCase(TestWithPermission):

    def setUp(self):
        super(TeacherPanelViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        teacher_1 = self.create_person('teacher')
        teacher_1.first_login = False
        teacher_1.save()
        self.client_2 = Client()
        self.client_2.login(
            username=teacher_1.user.username,
            password=self.password
        )

        teacher_2 = self.create_person('teacher')
        self.client_3 = Client()
        self.client_3.login(
            username=teacher_2.user.username,
            password=self.password
        )

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


class TeacherSubjectViewTestCase(TestWithPermission):

    def setUp(self):
        super(TeacherSubjectViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        self.teacher = self.create_person('teacher')
        self.client_2 = Client()
        self.client_2.login(
            username=self.teacher.user.username,
            password=self.password
        )
        self.student = self.create_person('student')
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
        form_data = {'grade': 4, 'weight': 7, 'student': self.student.user.id}
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
            response,
            f'/yourgrades/teachersubject/{self.subject.unique_code}'
        )

        # Checking creation mail with info about new grade
        self.assertTrue(
            MailboxReceived.objects.filter(sender__user=self.teacher.user)
        )


class CreateMessageViewTestCase(TestWithPermission):

    def setUp(self):
        super(CreateMessageViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )
        self.teacher = self.create_person('teacher')
        self.teacher.first_login = False
        self.teacher.save()

        self.client_2 = Client()
        self.client_2.login(
            username=self.teacher.user.username,
            password=self.password
        )
        self.student = self.create_person('student')

    def test_create_message(self):
        # GET, user without student/parent/teacher/manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:create_message',
                kwargs={
                    'prefix': 1,
                    'code': self.student.school_class.unique_code
                }
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
            MailboxReceived.objects.filter(
                sender__user=self.teacher.user,
                recipient__user=self.student.user
            )
        )
        message = MailboxReceived.objects.get(
            sender__user=self.teacher.user,
            recipient__user=self.student.user
        ).message
        self.assertEqual(message.subject, form_data['subject'])
        self.assertEqual(message.text, form_data['text'])


class MailboxViewTestCase(TestWithPermission):

    def setUp(self):
        super(MailboxViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )
        self.parent = self.create_person('parent')
        self.client_2 = Client()
        self.client_2.login(
            username=self.parent.user.username,
            password=self.password
        )

    def test_mailbox(self):
        # GET, user without student/parent/teacher/manager permission -> 403
        response = self.client_1.get(reverse('yourgrades:mailbox'))
        self.assertEqual(response.status_code, 403)

        # GET, user with student/parent/teacher/manager permission -> 200
        response = self.client_2.get(reverse('yourgrades:mailbox'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/mailbox.html')


class MailTextViewTestCase(TestWithPermission):

    def setUp(self):
        super(MailTextViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )
        self.student = self.create_person('student')
        self.client_2 = Client()
        self.client_2.login(
            username=self.student.user.username,
            password=self.password
        )
        self.teacher = self.create_person('teacher')
        message = Message.objects.create(
            subject='Test subject',
            text='Test text.'
        )
        recipient = Recipient.objects.create(
            user=self.student.user,
            message=message
        )
        sender = Sender.objects.create(user=self.teacher.user, message=message)
        self.mailbox_received = MailboxReceived.objects.create(
            sender=sender,
            recipient=recipient,
            message=message,
        )

    def test_mailbox(self):
        # GET, user without student/parent/teacher/manager permission -> 403
        response = self.client_1.get(
            reverse(
                'yourgrades:mail_text',
                kwargs={
                     'mailbox_id': self.mailbox_received.id,
                     'mailbox_type': 1
                 }
            )
        )
        self.assertEqual(response.status_code, 403)

        # GET, user with student/parent/teacher/manager permission -> 200
        # Mailbox type 1 (received)
        response = self.client_2.get(
            reverse(
                'yourgrades:mail_text',
                kwargs={
                    'mailbox_id': self.mailbox_received.id,
                    'mailbox_type': 1
                }
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/mailtext.html')
        # Checking if message is read
        self.assertEqual(
            MailboxReceived.objects.get(id=self.mailbox_received.id).read,
            True
        )

        # Mailbox type 2 (sent)
        new_message = Message.objects.create(
            subject='Test subject 2',
            text='Test text 2.'
        )
        mailbox_sent = MailboxSent.objects.create(
            sender=Sender.objects.create(
                user=self.student.user,
                message=new_message
            ),
            recipient='Jan Kowalski',
            message=new_message
        )
        response = self.client_2.get(
            reverse(
                'yourgrades:mail_text',
                kwargs={'mailbox_id': mailbox_sent.id, 'mailbox_type': 2}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yourgrades/mailtext.html')


class StudentParentViewTestCase(TestWithPermission):

    def setUp(self):
        super(StudentParentViewTestCase, self).setUp()
        user = self.create_user()
        self.client_1 = Client()
        self.client_1.login(
            username=user.username,
            password=self.password
        )

        self.parent = self.create_person('parent')
        self.parent.first_login = False
        self.parent.save()
        self.client_2 = Client()
        self.client_2.login(
            username=self.parent.user.username,
            password=self.password
        )

        self.student = self.create_person('student')
        self.student.first_login = False
        self.student.save()
        self.client_3 = Client()
        self.client_3.login(
            username=self.student.user.username,
            password=self.password
        )

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
