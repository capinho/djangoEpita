from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import *
from django.forms import BaseModelFormSet


class StaffAddForm(UserCreationForm):
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label = "Addresse",
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label = "Numero Mobile.",
    )

    firstname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label = "Prénom",
    )

    lastname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label = "Nom",
    )

    email = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label = "Email",
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_lecturer = True
        user.first_name = self.cleaned_data.get('firstname')
        user.last_name = self.cleaned_data.get('lastname')
        user.phone = self.cleaned_data.get('phone')
        user.address = self.cleaned_data.get('address')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


class StudentAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label = "Nom utilisateur",
    )
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label = "Addresse",
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label = "Numero Mobile",
    )

    firstname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label = "Prénom",
    )

    lastname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label = "Nom",
    )

    level = forms.CharField(
        widget=forms.Select(
            choices = LEVEL,
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
            }
        ),
        label = "Addresse Email",
    )

    class Meta(UserCreationForm.Meta):
        model = User


    @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name=self.cleaned_data.get('firstname') 
        user.last_name=self.cleaned_data.get('lastname')
        user.phone=self.cleaned_data.get('phone')
        user.email=self.cleaned_data.get('email')
        user.save()
        student = Student.objects.create(user=user, id_number=user.username, level=self.cleaned_data.get('level'))
        student.save()
        return user


class CourseAddForm(forms.ModelForm):
    courseTitle = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label = "*Course Title",
    )
    courseCode = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label = "*Code de cours",
    )

    courseUnit = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label = "*Unité de cours",
    )

    description = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label = "Ajoutez une petite description",
        required = False,
    )

    level = forms.CharField(
        widget=forms.Select(
            choices = LEVEL,
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
        label = "*Niveau",
    )

    semester = forms.CharField(
        max_length=30,
        widget=forms.Select(
            choices=SEMESTER,
            attrs={
                'class': 'form-control',
            }
        ),
        label = "*Semestre",
    )

    is_elective = forms.BooleanField(label = "*is_elective", required=False)
    class Meta:
        model = Course
        fields = ['courseCode', 'courseTitle', 'courseUnit', 'level', 'description', 'semester', 'is_elective']



class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Ancien mot de passe",
        required=True)

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Nouveau mot de passe",
        required=True)
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirmer nouveau mot de passe",
        required=True)

    class Meta:
        model = User
        fields = ['id', 'password', 'password1', 'password2']

    def clean(self):
        super(ChangePasswordForm, self).clean()
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        id = self.cleaned_data.get('id')
        user = User.objects.get(pk=id)
        if not user.check_password(password):
            self._errors['password'] = self.error_class([
                'L\'ancien mot de passe ne correspond pas'])
        if password1 and password1 != password2:
            self._errors['password1'] = self.error_class([
                'Les mots de passe ne correspondent pas'])
        return self.cleaned_data


class CourseAllocationForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all().order_by('level'),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    lecturer = forms.ModelChoiceField(
        queryset=User.objects.filter(is_lecturer=True),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        label="Maître de conférences",
    )
    
    class Meta:
       model = CourseAllocation
       fields = ['lecturer', 'courses']

    def __init__(self, *args, **kwargs):
       user = kwargs.pop('user')
       super(CourseAllocationForm, self).__init__(*args, **kwargs)
       self.fields['lecturer'].queryset = User.objects.filter(is_lecturer=True)



class CourseRegitsrationForm(forms.ModelForm):
    class Meta:
        model = TakenCourse
        fields = ('course', )
        widgets = {
            'course': forms.CheckboxSelectMultiple
        }


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Prénom",
        max_length=30,
        required=False)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Nom",
        max_length=30,
        required=False)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Email",
        max_length=75,
        required=False)
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Numero telephone",
        max_length=16,
        required=False)

    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Adresse du domicile",
        max_length=200,
        required=False)

    picture = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Charger une photo",
        required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'phone', 'address', 'picture']

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['session']

class SemesterForm(forms.ModelForm):
    semester = forms.CharField(
        widget=forms.Select(
            choices = SEMESTER,
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
        label = "semestre",
    )
    is_current_semester = forms.CharField(
        widget=forms.Select(
            choices = ((True, 'Yes'), (False, 'No')),
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
        label = "le semestre est-il en cours?",
    )
    session = forms.ModelChoiceField(
        queryset=Session.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
        required=True
    )

    next_semester_begins = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'type': 'date',
            }
        ),
        required=True)
    class Meta:
        model = Semester
        fields = ['semester', 'is_current_semester', 'session', 'next_semester_begins']