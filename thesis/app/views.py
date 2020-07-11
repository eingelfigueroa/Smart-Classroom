from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from scipy import misc
import sys
import os
import argparse
import tensorflow as tf
import numpy as np
import copy
import math
import pickle
from sklearn.svm import SVC
from sklearn.externals import joblib
import time
import random
from time import sleep
import cv2
import matplotlib.pyplot as plt
from os.path import join as pjoin

from . import save_image
from . import facenet
from . import detect_face
from . import create_classifier
from . import align_img
from . import face_recog
from . import attendance

from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import *
from .decorators import admin_only
from .forms import *
import errno
import copy
from thesis.settings import BASE_DIR
from django.db import IntegrityError
from django.db.models import Min, Q, F
from django.db.models.functions import ExtractDay, ExtractHour
from datetime import datetime, timedelta

######### AI Related Imports
def align(request):
	
	aligning = align_img.align

	aligning()

	context = {}

	return render(request, 'app/align.html', context)


def upload(request):
	base = BASE_DIR + '/app/train_img/'

	if request.method == 'POST':

		folder = request.POST['name']
		uploaded_file = request.FILES['document']
		path = os.path.join(base, folder)
		print(path)
		try:
			os.mkdir(path)
		except OSError as e:
			if e.errno == errno.EEXIST:
				redirect('app/upload.html')
			else:
				raise

		fs = FileSystemStorage(location=path)
		fs.save(uploaded_file.name, uploaded_file)

	data_dir = base

	for folder in os.listdir(data_dir):
		i = 1
		print(folder)
		fold = data_dir + '/' + folder
		for img in os.listdir(fold):
			extension = img.split(".")[-1].lower()
			# if extension != "jpeg":
			#    continue
			if i == 0:
				stri = '000'
			elif 0 < i < 10:
				stri = '00' + str(i)
			elif 9 < i < 99:
				stri = '0' + str(i)
			else:
				stri = str(i)
			extension = 'jpg'
			os.rename(os.path.join(fold, img), os.path.join(
				fold, os.path.basename(fold) + "_0" + stri + '.' + extension))
			i = i + 1

	return render(request, 'app/upload.html')


def MakeAttendance(request):
	attendance = attendance.Recog_attendance


	attendance()
	
	return render(request, 'app/attendance.html')

def classifier(request):
	classifying = create_classifier.classification


	classifying()
	
	return render(request, 'app/classify.html')

def detection(request):
	detected = face_recog.detection

	detected()
	messages.success(request, ' The recognition is done')

	return render(request, 'app/detect.html')

#################################################################


################## User Pages #####################

@login_required(login_url='login')
@admin_only
def home(request):


	return render(request, 'app/dashboard.html')






def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				user = form.save()
				print(user)
				username = form.cleaned_data.get('username')
				
				Staff.objects.create(
					user=user,
					name=user.username,
				)
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'app/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'app/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def accountSettings(request):
	staff = request.user
	form = StaffForm(instance=staff)

	if request.method == 'POST':
		form = StaffForm(request.POST,instance=staff)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'app/account_settings.html', context)


def notFound(request):

	return render(request, 'app/404.html')

def technical(request):

	return render(request, 'app/technical.html')

def example(request):

	instructors = Staff.objects.filter(is_active=1)

	content = {
		'instructors':instructors
	}

	return render(request, 'app/example.html', content)

def exampleSection(request, pk):
	int_now = datetime.now().day
	instructors_section = Section.objects.filter(Q(course_staff_fk__staff_fk=pk)).all()
	
	rec_sec = Recorded.objects.annotate(day_now=ExtractDay('time_detected')).filter(day_now=int_now)

	content = {
		'instructors_section': instructors_section,
		'rec_sec': rec_sec,
		
	}

	return render(request, 'app/example_section.html', content)

def section(request, pk):

    sections = Section.objects.filter(Q(course_staff_fk__staff_fk = pk)).all()
    
    context = {
        'sections':sections
    }

    return render(request, 'app/section.html', context)


def sectionStudent(request, pk):

    students = StudentAttendance.objects.filter(section_fk=pk).all()
    section_code = Section.objects.get(id=pk)
    
    context = {
        'students': students,
        'section_code':section_code,
        
    }

    return render(request, 'app/students.html', context)

def testing(request):

	return render(request, 'app/test.html')

######################### FORMS ############################

def add_students(request):
	form = StudentForm()
	if request.method == 'POST':
		form = StudentForm(request.POST)
		if form.is_valid():
			user = form.save()
			name = form.cleaned_data.get('name')
			messages.success(request, 'Student was created for ' + name)

			return redirect('add_student')
		

	context = {'form':form}
	return render(request, 'app/add_students.html', context)

def add_courses(request):
	form = CourseForm()
	if request.method == 'POST':
		form = CourseForm(request.POST)
		if form.is_valid():
			user = form.save()
			name = form.cleaned_data.get('name')
			messages.success(request, 'Course '+ name + "created")

			return redirect('add_course')
		

	context = {'form':form}
	return render(request, 'app/add_course.html', context)

def add_classrooms(request):
	form = RoomForm()
	if request.method == 'POST':
		form = RoomForm(request.POST)
		if form.is_valid():
			user = form.save()
			name = form.cleaned_data.get('name')
			messages.success(request, 'Created Room no. ' + name)

			return redirect('add_classroom')
		

	context = {'form':form}
	return render(request, 'app/add_classroom.html', context)

def add_schedules(request):
	form = ScheduleForm()
	if request.method == 'POST':
		form = ScheduleForm(request.POST)
		if form.is_valid():
			user = form.save()
			
			messages.success(request, 'Schedule Created')

			return redirect('add_schedule')
		

	context = {'form':form}
	return render(request, 'app/add_schedule.html', context)

def add_sections(request):  #####NEEDS Configurations

	form = SectionForm()
	if request.method == 'POST':
		form = SectionForm(request.POST)
		if form.is_valid():
			form.save()
			
			messages.success(request, 'Section Created')

			return redirect('add_section')
	
		

	context = {'form':form}
	return render(request, 'app/add_section.html', context)