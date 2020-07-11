from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from .models import *

class TimeInput(forms.TimeInput):
    input_type = "time"

class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y"
        super().__init__(**kwargs)

class CourseForm(ModelForm):

    class Meta:
        model = Course
        fields = '__all__'







class SectionForm(ModelForm):

   # def __init__(self, *args, **kwargs):
      #  super(SectionForm, self).__init__(*args, **kwargs)
        #self.fields['course_staff_fk'].queryset = Course.objects.filter(staff_fk=course_staff_fk)

    class Meta:
        model = Section
        fields = '__all__'
        

    





class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["time_start"].widget = TimeInput()
        self.fields["time_end"].widget = TimeInput()
        


class RoomForm(ModelForm):
    class Meta:
        model = Classroom
        fields = '__all__'


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'




class StaffForm(ModelForm):
	class Meta:
		model = Staff
		fields = ['username','fullname','department_fk']
		

class CreateUserForm(UserCreationForm):
	
	
	class Meta:
		model = Staff
		fields = ['username', 'email','department_fk', 'password1', 'password2']



class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Staff
        fields = ('email','username','fullname', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]