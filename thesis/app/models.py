from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyStaffManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
       

        user = self.model(
                email=self.normalize_email(email),
                username=username,
                
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
 
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            
            
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Department(models.Model):
    name = models.CharField(max_length=55)
    code = models.CharField(max_length=55)

    def __str__(self):
        return self.name

class Staff(AbstractBaseUser):
    
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name="Date Joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last Login", auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    fullname = models.CharField(max_length=60)
    position = models.CharField(max_length=45)
    department_fk = models.ForeignKey(
        Department, models.CASCADE, db_column='department_fk', default=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
    
    objects = MyStaffManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Course(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    staff_fk = models.ForeignKey('Staff', models.CASCADE)

    def __str__(self):
        return '%s,%s' %(self.name, self.staff_fk)


class Classroom(models.Model):
    name = models.CharField(max_length=22)
    course_fk = models.ForeignKey(
        'Course', models.CASCADE, db_column='course_fk')

    def __str__(self):
        return self.name


class CourseHasStudent(models.Model):
    course = models.ForeignKey(Course, models.CASCADE)
    student = models.ForeignKey('Student', models.CASCADE)


class Schedule(models.Model):

    DAYS = (
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),

    )
    day = models.CharField(max_length=22, choices=DAYS)
    time_start = models.TimeField()
    time_end = models.TimeField()
    classroom_fk = models.ForeignKey(
        Classroom, models.CASCADE, db_column='classroom_fk')

    def __str__(self):
        return '%s %s %s %s' % (self.day, self.time_start, self.time_end, self.classroom_fk)

class Section(models.Model):
    SEM = (
        ('1st', '1st'),
        ('2nd', '2nd'),
        ('Summer','Summer'),
    )

    section_code = models.CharField(max_length=22)
    academic_year = models.CharField(max_length=22)
    semester = models.CharField(max_length=22, choices=SEM)
    course_fk = models.ForeignKey(
        Course, models.CASCADE, db_column='course_fk')
    course_staff_fk = models.ForeignKey(
        Course, models.CASCADE, db_column='course_staff', related_name='course_staff')
    schedule_fk = models.ForeignKey(
        Schedule, models.CASCADE, db_column='schedule_fk')
    scheduleClassroom_fk = models.ForeignKey(
        Schedule, models.CASCADE, db_column='schedule_classroom_fk', related_name='classroom_schedule')

    def __str__(self):
        return self.section_code


class Student(models.Model):
    
    name = models.CharField(max_length=22)
    student_id = models.CharField(max_length=22)
    department_fk = models.ForeignKey(
        Department, models.CASCADE, db_column='department_fk')

    def __str__(self):
        return self.name

class Recorded(models.Model):

    student_name = models.CharField(max_length=22)
    time_detected = models.DateTimeField()
    image = models.BinaryField()

    def __str__(self):
        return self.time_detected


class StudentAttendance(models.Model):

    attendance_on_time = models.IntegerField()
    attendance_late = models.IntegerField()
    attendance_absent = models.IntegerField()
    attendance_suspended = models.IntegerField()
    student_fk = models.ForeignKey(
        Student, models.CASCADE, db_column='student_fk')
    section_fk = models.ForeignKey(
        Section, models.CASCADE, db_column='section_fk')
    section_course_fk = models.ForeignKey(
        Section, models.CASCADE, db_column='section_course_fk', related_name="section_course")
    section_course_staff_fk = models.ForeignKey(
        Section, models.CASCADE, db_column='section_course_staff_fk', related_name="section_staff")
    section_schedule_fk = models.ForeignKey(
        Section, models.CASCADE, db_column='section_schedule_fk', related_name="section_schedule")
    section_schedule_classroom_fk = models.ForeignKey(
        Section, models.CASCADE, db_column='section_schedule_classroom_fk', related_name="section_classroom")

    def __str__(self):
        return '%s %s %s %s' % (self.section_fk, self.student_fk, self.section_course_fk, self.section_schedule_fk)
