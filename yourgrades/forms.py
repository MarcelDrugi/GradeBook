from django import forms
from django.core.validators import RegexValidator
from .models import *


class SchoolClassForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SchoolClassForm, self).__init__(*args, **kwargs)
        self.fields['unique_code'].widget = forms.HiddenInput()
        self.fields['name'].widget = forms.TextInput(
            attrs={'placeholder': 'np. 1a', 'class': 'form-control input-sm'}
        )
        self.fields['year'].widget = forms.NumberInput(
            attrs={
                'placeholder': 'np. 1990',
                'class': 'form-control input-sm'
            }
        )

    unique_code = forms.CharField(
        max_length=6,
        validators=[RegexValidator(r'^[1-8]{1}[a-z]{1}[0-9]{4}$')],
        help_text='Format: class name + year e.g.: 1b2019',
        required=False
    )

    class Meta:
        model = SchoolClass
        fields = ['name', 'year', 'unique_code']
        labels = {
            'name': 'nazwa klasy',
            'unique_code': 'kod klasy',
            'year': 'rok zakończenia nauki'
        }


class CreateStudentForm(forms.Form):
    name = forms.CharField(
        max_length=64,
        label='Imię ucznia:',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'wprowadź imię',
                'class': 'form-control'
            }
        )
    )
    surname = forms.CharField(
        max_length=64,
        label='Nazwisko ucznia:',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'wprowadź nazwisko',
                'class': 'form-control'
            }
        )
    )
    birthday = forms.DateField(
        label='Data urodzenia (rrrr-mm-dd):',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'wprowadź datę',
                'class': 'form-control'
            }
        )
    )
    first_parent_name = forms.CharField(
        max_length=64,
        label='Imię rodzica:',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'wprowadź imię',
                'class': 'form-control'
            }
        )
    )
    first_parent_surname = forms.CharField(
        max_length=64,
        label='Nazwosko rodzica:',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'wprowadź nazwisko',
                'class': 'form-control'
            }
        )
    )
    second_parent_name = forms.CharField(
        max_length=64,
        required=False,
        label='Imię drugiego rodzica:',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'wprowadź imię',
                'class': 'form-control'
            }
        )
    )
    second_parent_surname = forms.CharField(
        max_length=64,
        required=False,
        label='Nazwosko drugiego rodzica:',
        widget=forms.TextInput(
            attrs={
                'placeholder':'wprowadź nazwisko',
                'class': 'form-control'
            }
        )
    )


class CreateTeacherForm(forms.Form):
    name = forms.CharField(
        max_length=64,
        label='Imię:',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'wprowadź imię',
                'class': 'form-control'
            }
        )
    )
    surname = forms.CharField(
        max_length=64,
        label='Naziwsko:',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'wprowadź imię',
                'class': 'form-control'
            }
        )
    )


class CreateSubjectForm(forms.Form):
    name = forms.CharField(
        max_length=128,
        label='Nazwa',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'wprowadź nazwę',
                'class': 'form-control'
            }
        )
    )
    shortcut = forms.CharField(
        max_length=2,
        label='Skrót',
        help_text='Dwuliterowy skrót nazwy przedmiotu',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'wprowadź dwuliterowy skrót',
                'class': 'form-control'
            }
        )
    )
    teachers = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': ''}),
        queryset=Teacher.objects.filter(active=True),
        required=False,
        label='Wybierz nauczycieli'
    )


class AddSubjectTeacherForm(forms.Form):
    teachers = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Teacher.objects.filter(active=True)
    )


class AddGradeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddGradeForm, self).__init__(*args, **kwargs)
        self.fields['grade'].widget = forms.NumberInput(
            attrs={'placeholder': 'ocena  1 - 6',
                   'class': 'form-control input-sm'}
        )
        self.fields['weight'].widget = forms.NumberInput(
            attrs={'placeholder': 'waga  1 - 10',
                   'class': 'form-control input-sm'}
        )

    class Meta:
        model = Grades
        fields = ['grade', 'weight']
        labels = {'grade': 'ocena: ', 'weight': 'waga: '}


class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['subject'].widget = forms.TextInput(
            attrs={'placeholder': 'Wpisz tytuł wiadomości',
                   'class': 'form-control input-sm'}
        )
        self.fields['text'].widget = forms.Textarea(
            attrs={'placeholder': 'Wpisz tekst wiadomości',
                   'class': 'form-control input-sm'}
        )

    class Meta:
        model = Message
        fields = {'subject', 'text'}
        labels = {'subject': 'Temat: ', 'text': 'Treść wiadomości: '}


class LoginForm(forms.Form):
    username = forms.CharField(
        label='login:',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'wprowadź login',
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        label='haslo:',
        min_length=5,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'wprowadź hasło',
                'class': 'form-control'
            }
        )
    )


class FirstLoginForm(forms.Form):
    username = forms.CharField(
        label='login',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'wprowadź login',
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        label='haslo',
        min_length=5,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'wprowadź hasło',
                'class': 'form-control'
            }
        )
    )
    password_confirm = forms.CharField(
        label=' potwierdź haslo',
        min_length=5,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'potwierdzenie',
                'class': 'form-control'
            }
        )
    )


class AddSubjectDateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddSubjectDateForm, self).__init__(*args, **kwargs)
        self.fields['day'].widget.attrs['class'] = 'form-control input-sm'
        self.fields['lesson_number'].widget.attrs['class'] = \
            'form-control input-sm'

    class Meta:
        model = SubjectDate
        fields = ['day', 'lesson_number']
        labels = {'day': 'dzień tygodnia: ', 'lesson_number': 'lekcja: ', }
