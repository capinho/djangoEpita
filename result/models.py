from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.conf import settings
from .validators import ASCIIUsernameValidator

TB = "Très Bien"
B = "Bien"
M = "Moyen"
I = "Insuffisant"
TI = "Tres Insuffisant"
PASS = "REUSSITE"
FAIL = "ECHEC"

GRADE = (
		(TB, 'Très Bien'),
		(B, 'Bien'),
		(M, 'Moyen'),
		(I, 'Insuffisant'),
		(TI, 'Tres Insuffisant'),
	)

COMMENT = (
		(PASS, "REUSSITE"),
		(FAIL, "ECHEC"),
	)

LEVEL = (
		("INFOSUP", 'INFOSUP'),
		("INFOSPE", 'INFOSPE'),
		("ING1", 'ING1'),
		("ING2", 'ING2'),
		("ING3", 'ING3'),
	)
FIRST = "First"
SECOND = "Second"

SEMESTER = (
		(FIRST, "First"),
		(SECOND, "Second"),
	)

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    phone = models.CharField(max_length=60, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    picture = models.ImageField(upload_to="pictures/", blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    username_validator = ASCIIUsernameValidator()

    def get_picture(self):
        no_picture = settings.STATIC_URL + 'img/img_avatar.png'
        try:
            return self.picture.url
        except:
            return no_picture

    def get_full_name(self):
        full_name = self.username
        if self.first_name and self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name

class Session(models.Model):
    session = models.CharField(max_length=200, unique=True)
    is_current_session = models.BooleanField(default=False, blank=True, null=True)
    next_session_begins = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.session

class Semester(models.Model):
    semester = models.CharField(max_length=10, choices=SEMESTER, blank=True)
    is_current_semester = models.BooleanField(default=False, blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)
    next_semester_begins = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.semester


class Course(models.Model):
    courseTitle = models.CharField(max_length=200)
    courseCode = models.CharField(max_length=200, unique=True)
    courseUnit = models.CharField(max_length=200)
    description = models.TextField(max_length=200, blank=True)
    level = models.CharField(choices=LEVEL, max_length=12, blank=True)
    semester = models.CharField(choices=SEMESTER, max_length=200)
    is_elective = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.courseCode + " (" + self.courseTitle + ")"

    def get_absolute_url(self):
        return reverse('course_list', kwargs={'pk': self.pk})

    def get_total_unit(self):
        t = 0
        total = Course.objects.all()
        for i in total:
            t +=i
        return i

class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	id_number = models.CharField(max_length=20, unique=True)
	level = models.CharField(choices=LEVEL, max_length=12)

	def __str__(self):	
		return self.id_number

	def get_absolute_url(self):
		return reverse('profile')

class TakenCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='taken_courses')
    ca = models.PositiveIntegerField(blank=True, null=True, default=0)
    exam = models.PositiveIntegerField(blank=True, null=True, default=0)
    total = models.PositiveIntegerField(blank=True, null=True, default=0)
    grade = models.CharField(choices=GRADE, max_length=1, blank=True)
    comment = models.CharField(choices=COMMENT, max_length=200, blank=True)

    def get_absolute_url(self):
        return reverse('update_score', kwargs={'pk': self.pk})


    def get_total(self, ca, exam):
        return (float(ca) + 2*float(exam)) / 3

    def get_grade(self, ca, exam):
    	total = (float(ca) + 2*float(exam)) / 3
    	if total >= 17:
    		grade = TB
    	elif total >= 14:
    		grade = B
    	elif total >=10:
    		grade = M
    	elif total >=6:
    		grade = I
    	else:
    	 	grade = TI
    	return grade

    def get_comment(self, grade):
        if not grade == "TI":
            comment = PASS
        else:
            comment = FAIL
        return comment

    def carry_over(self, grade):
        if grade == TI:
            CarryOverStudent.objects.get_or_create(student=self.student, course=self.course)
        else:
            try:
                CarryOverStudent.objects.get(student=self.student, course=self.course).delete()
            except:
                pass

    def is_repeating(self):
        count = CarryOverStudent.objects.filter(student__id=self.student.id)
        units = 0
        for i in count:
            #units += int(i.course.courseUnit)
            units += int(i.course.id)
        if count.count() >= 6 or units >=16:
            RepeatingStudent.objects.get_or_create(student=self.student, level=self.student.level)
        else:
            try:
                RepeatingStudent.objects.get(student=self.student, level=self.student.level).delete()
            except:
                pass

    def calculate_gpa(self, total_unit_in_semester):
        current_semester = Semester.objects.get(is_current_semester=True)
        student = TakenCourse.objects.filter(student=self.student, course__level=self.student.level, course__semester=current_semester)
        p = 0
        point = 0
        for i in student:
            #courseUnit = i.course.courseUnit
            courseUnit = i.course.id
            total = i.total
            '''if i.grade == TB:
                point = 5
            elif i.grade == B:
                point = 4
            elif i.grade == M:
                point = 3
            elif i.grade == I:
                point = 2
            else:
                point = 0'''
            p += int(courseUnit) * total
            #p += int(total)
        try:
            gpa = (p / total_unit_in_semester)
            return round(gpa, 1)
        except ZeroDivisionError:
            return 0
    
    def calculate_cgpa(self):
        current_semester = Semester.objects.get(is_current_semester=True)
        previousResult = Result.objects.filter(student__id=self.student.id, level__lt=self.student.level)
        previousCGPA = 0
        for i in previousResult:
            if i.cgpa is not None:
                previousCGPA += i.cgpa
        cgpa = 0
        if str(current_semester) == SECOND:
            try:
                first_sem_gpa = Result.objects.get(student=self.student.id, semester=FIRST, level=self.student.level) 
                first_sem_gpa += first_sem_gpa.gpa.gpa
            except:
                first_sem_gpa = 0

            try:
                sec_sem_gpa = Result.objects.get(student=self.student.id, semester=SECOND, level=self.student.level) 
                sec_sem_gpa += sec_sem_gpa.gpa
            except:
                sec_sem_gpa = 0

            taken_courses = TakenCourse.objects.filter(student=self.student, student__level=self.student.level)
            TCU = 0
            for i in taken_courses:
                #TCU += int(i.course.courseUnit)
                TCU += int(i.course.id)
            cpga = first_sem_gpa + sec_sem_gpa / TCU
            
            return round(cgpa, 2)


class CourseAllocation(models.Model):
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, related_name='allocated_course')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.lecturer.username

class CarryOverStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=100, choices=SEMESTER, blank=True, null=True)
    session = models.CharField(max_length=100, blank=True, null=True)
    level = models.CharField(choices=LEVEL, max_length=12, blank=True, null=True)

    def __str__(self):
        return self.student.id_number


class RepeatingStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    level = models.CharField(max_length=100, choices=LEVEL)
    session = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.student.id_number

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    gpa = models.FloatField(null=True)
    cgpa = models.FloatField(null=True)
    semester = models.CharField(max_length=100, choices=SEMESTER)
    session = models.CharField(max_length=100, blank=True, null=True)
    level = models.CharField(max_length=100, choices=LEVEL)
