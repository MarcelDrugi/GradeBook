from django.test import TestCase
from django.urls import resolve, reverse


class URLTestCase(TestCase):
    def test_homepage(self):
        url = '/yourgrades'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:homepage')
        self.assertEqual(reverse('yourgrades:homepage'), url)

    def test_manager(self):
        url = '/yourgrades/manager'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:manager')
        self.assertEqual(reverse('yourgrades:manager'), url)

    def test_create_school_class(self):
        url = '/yourgrades/manager/creaateschoolclass'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:create_school_class')
        self.assertEqual(reverse('yourgrades:create_school_class'), url)

    def test_edit_school_class(self):
        class_unique_code = '1a2024'
        url = f'/yourgrades/manager/editschoolclass/{class_unique_code}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:edit_school_class')
        self.assertEqual(
            reverse(
                'yourgrades:edit_school_class',
                kwargs={'class_unique_code': class_unique_code}),
            url
        )

    def test_del_student(self):
        user_id = '514'
        url = f'/yourgrades/manager/delstudent/{user_id}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:del_student')
        self.assertEqual(
            reverse(
                'yourgrades:del_student',
                kwargs={'user_id': user_id}),
            url
        )

    def test_deactivation_school_class(self):
        class_unique_code = '3b2021'
        url = f'/yourgrades/manager/deactivationschoolclass' \
              f'/{class_unique_code}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:deactivation_school_class')
        self.assertEqual(
            reverse(
                'yourgrades:deactivation_school_class',
                kwargs={'class_unique_code': class_unique_code}),
            url
        )

    def test_activation_school_class(self):
        class_unique_code = '2c2022'
        url = f'/yourgrades/manager/activationschoolclass/{class_unique_code}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:activation_school_class')
        self.assertEqual(
            reverse(
                'yourgrades:activation_school_class',
                kwargs={'class_unique_code': class_unique_code}),
            url
        )

    def test_deactivation_teacher(self):
        teacher_user_id = '349'
        url = f'/yourgrades/manager/deactivationteacher/{teacher_user_id}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:deactivation_teacher')
        self.assertEqual(
            reverse(
                'yourgrades:deactivation_teacher',
                kwargs={'teacher_user_id': teacher_user_id}),
            url
        )

    def test_activation_teacher(self):
        teacher_user_id = '349'
        url = f'/yourgrades/manager/activationteacher/{teacher_user_id}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:activation_teacher')
        self.assertEqual(
            reverse(
                'yourgrades:activation_teacher',
                kwargs={'teacher_user_id': teacher_user_id}),
            url
        )

    def test_add_teacher(self):
        url = '/yourgrades/manager/addteacher'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:add_teacher')
        self.assertEqual(reverse('yourgrades:add_teacher'), url)

    def test_add_subject(self):
        class_unique_code = '5f2024'
        url = f'/yourgrades/manager/editschoolclass/{class_unique_code}' \
              f'/addsubject'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:add_subject')
        self.assertEqual(
            reverse(
                'yourgrades:add_subject',
                kwargs={'class_unique_code': class_unique_code},
            ),
            url
        )

    def test_manager_student_edit(self):
        user_id = 13
        url = f'/yourgrades/manager/editstudent/{user_id}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:manager_student_edit')
        self.assertEqual(
            reverse(
                'yourgrades:manager_student_edit',
                kwargs={'user_id': user_id},
            ),
            url
        )

    def test_manager_reset_user(self):
        user_id = 227
        prefix = 2
        url = f'/yourgrades/manageresetusesr/{prefix}/{user_id}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:manager_reset_user')
        self.assertEqual(
            reverse(
                'yourgrades:manager_reset_user',
                kwargs={'user_id': user_id, 'prefix': prefix, },
            ),
            url
        )

    def test_subject_view(self):
        class_unique_code = '2f2024'
        subject_unique_code = 'Hi2f2024'
        url = f'/yourgrades/manager/editschoolclass/{class_unique_code}/' \
              f'{subject_unique_code}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:subject_view')
        self.assertEqual(
            reverse(
                'yourgrades:subject_view',
                kwargs={
                    'class_unique_code': class_unique_code,
                    'subject_unique_code': subject_unique_code,
                },
            ),
            url
        )

    def test_delete_date(self):
        class_unique_code = '1b2025'
        subject_unique_code = 'Ge1b2025'
        day = 2
        lesson = 4
        url = f'/yourgrades/manager/deldate/{class_unique_code}/' \
              f'{subject_unique_code}/{day}/{lesson}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:delete_date')
        self.assertEqual(
            reverse(
                'yourgrades:delete_date',
                kwargs={
                    'class_unique_code': class_unique_code,
                    'subject_unique_code': subject_unique_code,
                    'day': day,
                    'lesson': lesson,
                },
            ),
            url
        )

    def test_del_subject(self):
        class_unique_code = '3a2024'
        subject_unique_code = 'Ma3a2024'
        url = f'/yourgrades/manager/delsubject/{class_unique_code}/' \
              f'{subject_unique_code}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:del_subject')
        self.assertEqual(
            reverse(
                'yourgrades:del_subject',
                kwargs={
                    'class_unique_code': class_unique_code,
                    'subject_unique_code': subject_unique_code,
                },
            ),
            url
        )

    def test_del_subject_teacher(self):
        class_unique_code = '3a2024'
        subject_unique_code = 'Ma3a2024'
        teacher_user_id = 95
        url = f'/yourgrades/delsubjectteacher/{class_unique_code}/' \
              f'{subject_unique_code}/{teacher_user_id}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:del_subject_teacher')
        self.assertEqual(
            reverse(
                'yourgrades:del_subject_teacher',
                kwargs={
                    'class_unique_code': class_unique_code,
                    'subject_unique_code': subject_unique_code,
                    'teacher_user_id': teacher_user_id,
                },
            ),
            url
        )

    def test_add_subject_teacher(self):
        class_unique_code = '1a2026'
        subject_unique_code = 'Ph1a2026'
        url = f'/yourgrades/addnewsubjectteacher/{class_unique_code}/' \
              f'{subject_unique_code}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:add_subject_teacher')
        self.assertEqual(
            reverse(
                'yourgrades:add_subject_teacher',
                kwargs={
                    'class_unique_code': class_unique_code,
                    'subject_unique_code': subject_unique_code,
                },
            ),
            url
        )

    def test_manager_teacher(self):
        teacher_user_id = '199'
        url = f'/yourgrades/manager/teacher/{teacher_user_id}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:manager_teacher')
        self.assertEqual(
            reverse(
                'yourgrades:manager_teacher',
                kwargs={'teacher_user_id': teacher_user_id}),
            url
        )

    def test_manager_teacher_edit(self):
        user_id = '199'
        url = f'/yourgrades/manager/editteacher/{user_id}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:manager_teacher_edit')
        self.assertEqual(
            reverse(
                'yourgrades:manager_teacher_edit',
                kwargs={'user_id': user_id}),
            url
        )

    def test_manager_del_teacher(self):
        teacher_user_id = '72'
        url = f'/yourgrades/manager/delteacher/{teacher_user_id}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:manager_del_teacher')
        self.assertEqual(
            reverse(
                'yourgrades:manager_del_teacher',
                kwargs={'teacher_user_id': teacher_user_id}),
            url
        )

    def test_teacher(self):
        url = '/yourgrades/teacher'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:teacher')
        self.assertEqual(reverse('yourgrades:teacher'), url)

    def test_teacher_subject(self):
        subject_unique_code = 'Ph1a2026'
        url = f'/yourgrades/teachersubject/{subject_unique_code}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:teacher_subject')
        self.assertEqual(
            reverse(
                'yourgrades:teacher_subject',
                kwargs={'subject_unique_code': subject_unique_code, },
            ),
            url
        )

    def test_timetable(self):
        person = 'student'
        url = f'/yourgrades/timetable/{person}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:timetable')
        self.assertEqual(
            reverse('yourgrades:timetable', kwargs={'person': person}),
            url
        )

    def test_mailbox(self):
        url = '/yourgrades/mailbox'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:mailbox')
        self.assertEqual(reverse('yourgrades:mailbox'), url)

    def test_mail_text(self):
        mailbox_id = 241
        mailbox_type = 1
        url = f'/yourgrades/mailtext/{mailbox_id}/{mailbox_type}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:mail_text')
        self.assertEqual(
            reverse(
                'yourgrades:mail_text',
                kwargs={'mailbox_id': mailbox_id, 'mailbox_type': mailbox_type}
            ),
            url
        )

    def test_student_parent(self):
        url = '/yourgrades/studentparent'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:student_parent')
        self.assertEqual(reverse('yourgrades:student_parent'), url)

    def test_first_login(self):
        url = '/yourgrades/firstlogin'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:first_login')
        self.assertEqual(reverse('yourgrades:first_login'), url)

    def test_logout(self):
        url = '/yourgrades/logout'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:logout')
        self.assertEqual(reverse('yourgrades:logout'), url)

    def test_create_message(self):
        prefix = 2
        code = '3c2023'
        url = f'/yourgrades/createmessage/{prefix}/{code}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:create_message')
        self.assertEqual(
            reverse(
                'yourgrades:create_message',
                kwargs={'prefix': prefix, 'code': code}
            ),
            url
        )

    def test_manager_student(self):
        user_id = '8172'
        url = f'/yourgrades/manager/student/{user_id}'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:manager_student')
        self.assertEqual(
            reverse(
                'yourgrades:manager_student',
                kwargs={'user_id': user_id}),
            url
        )

    def test_manager_history(self):
        url = '/yourgrades/manager/history'
        name = resolve(url).view_name
        self.assertEqual(name, 'yourgrades:manager_history')
        self.assertEqual(reverse('yourgrades:manager_history'), url)
